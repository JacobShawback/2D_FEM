#include "all.h"
#include <Eigen/Core>
#include "node.h"
#include "material.h"
#include "element_style.h"
#include "element.h"
#include "fem.h"
#include "io_data.h"
#include "input_wave.h"

int main() {

  clock_t start = clock();

  // ----- Input FEM Mesh ----- //
  Fem fem = io_data::input_mesh("input/mesh.in");
  auto outputs = io_data::input_outputs("input/output.in");
  std::string output_dir = "result/";

  // ----- FEM Set up ----- //
  fem.set_init();
  fem.set_output(outputs);

  // ----- Define input wave ----- //
  size_t fsamp = 5000;
  double fp = 0.2;
  double duration = 1.0/fp;

  Eigen::VectorXd tim, wave_acc;
  double dt;
  std::tie(tim, dt) = input_wave::linspace(0,duration,(int)(fsamp*duration));
  wave_acc = input_wave::simple_sin(tim,fp,0.1);
  // wave_acc = input_wave::ricker(tim,fp,1.0/fp,0.1);
  size_t ntim = tim.size();

  // ----- Static deformation ----- //
  fem.self_gravity();

  // ----- Prepare time solver ----- //
  fem.update_init(dt);

  Eigen::MatrixXd output_dispx = Eigen::MatrixXd::Zero(ntim,fem.output_nnode);
  Eigen::MatrixXd output_dispz = Eigen::MatrixXd::Zero(ntim,fem.output_nnode);
  Eigen::MatrixXd output_velx = Eigen::MatrixXd::Zero(ntim,fem.output_nnode);
  Eigen::MatrixXd output_velz = Eigen::MatrixXd::Zero(ntim,fem.output_nnode);

  // ----- time iteration ----- //
  Eigen::VectorXd acc0 = Eigen::Vector2d::Zero(fem.dof);
  Eigen::VectorXd vel0 = Eigen::Vector2d::Zero(fem.dof);

  for (size_t it = 0 ; it < ntim ; it++) {
    acc0[0] = wave_acc[it];
    // acc0[0] = 0.0;
    // vel0[0] += wave_acc[it]*dt ;

    fem.update_time(acc0,vel0);

    for (size_t i = 0 ; i < fem.output_nnode ; i++) {
      Node& node = fem.nodes[fem.output_nodes[i]];
      output_dispx(it,i) = node.u(0) - node.u0(0);
      output_dispz(it,i) = node.u(1) - node.u0(1);
      output_velx(it,i) = node.v(0);
      output_velz(it,i) = node.v(1);
    }

    if (it%1000 == 0) {
      std::cout << it << " t= " << it*dt << " ";
      std::cout << output_dispz(it,0) << "\n";
    }
  }

  clock_t end = clock();
  std::cout << "elapsed_time: " << (double)(end - start) / CLOCKS_PER_SEC << "[sec]\n";

  // --- Write output file --- //
  std::ofstream f(output_dir + "z0_vs20_md.disp");
  for (size_t it = 0 ; it < ntim ; it++) {
    f << tim(it) ;
    for (size_t i = 0 ; i < fem.output_nnode ; i++) {
      f << " " << output_dispz(it,i);
    }
    f << "\n";
  }
  f.close();

}
