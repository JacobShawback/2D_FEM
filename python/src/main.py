import matplotlib.pyplot as plt
import numpy as np
import time

import io_data
import input_wave
import plot_model

start = time.time()

## --- Input FEM Mesh --- ##
fem = io_data.input_mesh("input/mesh.in")
outputs = io_data.input_outputs("input/output.in")

## --- FEM Set up --- ##
fem.set_init()
fem.set_output(outputs)
# plot_model.plot_mesh(fem)


## --- Define input wave --- ##
fsamp = 2000
duration = 10.0

tim,dt = np.linspace(0,duration,int(fsamp*duration),endpoint=False,retstep=True)
horizontal_acc = input_wave.smoothed_ramp(tim,fp=10.0,tp=1./10.,amp=9.8*3.0/5.0)

# wave_acc = input_wave.tapered_sin(tim,fp=5.0,taper=0.2,duration=1.0,amp=1.0)
# wave_vel = np.cumsum(wave_acc) * dt
ntim = len(tim)

## --- Prepare time solver --- ##
fem.update_init(dt)
ax = plot_model.plot_mesh_update_init()

## Iteration ##
output_vel = np.zeros((ntim,fem.output_nnode))
output_strain = np.zeros((ntim,fem.output_nelem))

for it in range(len(tim)):
    acc0 = np.array([-horizontal_acc[it],0.0])

    fem.update_time(acc0)

    output_vel[it,:] = [node.v[1] for node in fem.output_nodes]
    output_strain[it,:] = [element.strain[0] for element in fem.output_elements]

    if it%10 == 0:
        plot_model.plot_mesh_update(ax,fem,1.)
        print(it,it*dt,output_vel[it,:])


plot_model.plot_mesh_update(ax,fem,1.,fin=True)

elapsed_time = time.time() - start
print ("elapsed_time: {0}".format(elapsed_time) + "[sec]")

# ## Output result ##
# plt.figure()
# plt.plot(tim,wave_vel)
# plt.plot(tim,output_vel[:,0])
# plt.show()
