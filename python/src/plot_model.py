import matplotlib.pyplot as plt

#--------------------------------------------------------#
def plot_mesh(fem,amp=1.0,margin=0.1,margin_bottom=0.1,margin_top=0.25):
    pc = ["gray","yellow","green","pink","lightblue"]

    fig,ax = plt.subplots(figsize=(6,4))

    x = [node.xyz[0] for node in fem.nodes]
    z = [node.xyz[1] for node in fem.nodes]

    area_x = max(x)-min(x)
    area_z = max(z)-min(z)

    ax.set_xlim([min(x)-margin*area_x,max(x)+margin*area_x])
    ax.set_ylim([max(z)+margin_bottom*area_z,min(z)-margin_top*area_z])
    ax.set_aspect('equal')

    for element in fem.elements:
        if element.dim == 2:
            ic = element.material_id % len(pc)

            f0 = (element.nodes[0].xyz[0], element.nodes[0].xyz[1])
            f1 = (element.nodes[1].xyz[0], element.nodes[1].xyz[1])
            f2 = (element.nodes[2].xyz[0], element.nodes[2].xyz[1])
            f3 = (element.nodes[3].xyz[0], element.nodes[3].xyz[1])

            fpoly = plt.Polygon((f0,f1,f2,f3),ec="k",fc=pc[ic])
            ax.add_patch(fpoly)

    rc = 0.01*area_z
    for node in fem.nodes:
        p = plt.Circle((node.xyz[0],node.xyz[1]),rc,color="k")
        ax.add_patch(p)

    plt.show()

#--------------------------------------------------------#
def plot_mesh_update_init():
    _,ax = plt.subplots(figsize=(6,4))
    ax.set_axisbelow(True)
    return ax

def plot_mesh_update(ax,fem,amp=1.0,margin=0.1,margin_bottom=0.1,margin_top=0.25,fin=False):
    pc = ["gray","yellow","green","pink","lightblue"]

    ax.cla()
    ax.grid()

    x = [node.xyz[0] for node in fem.nodes]
    z = [node.xyz[1] for node in fem.nodes]

    area_x = max(x)-min(x)
    area_z = max(z)-min(z)

    ax.set_xlim([min(x)-margin*area_x,max(x)+margin*area_x])
    ax.set_ylim([max(z)+margin_bottom*area_z,min(z)-margin_top*area_z])
    ax.set_aspect('equal')

    for element in fem.elements:
        if element.dim == 2:
            ic = element.material_id % len(pc)

            f0 = (element.nodes[0].xyz[0]+element.nodes[0].u[0]*amp, element.nodes[0].xyz[1]+element.nodes[0].u[1]*amp)
            f1 = (element.nodes[1].xyz[0]+element.nodes[1].u[0]*amp, element.nodes[1].xyz[1]+element.nodes[1].u[1]*amp)
            f2 = (element.nodes[2].xyz[0]+element.nodes[2].u[0]*amp, element.nodes[2].xyz[1]+element.nodes[2].u[1]*amp)
            f3 = (element.nodes[3].xyz[0]+element.nodes[3].u[0]*amp, element.nodes[3].xyz[1]+element.nodes[3].u[1]*amp)

            fpoly = plt.Polygon((f0,f1,f2,f3),ec="k",fc=pc[ic])
            ax.add_patch(fpoly)

    rc = 0.01*area_z
    for node in fem.nodes:
        p = plt.Circle((node.xyz[0]+node.u[0]*amp,node.xyz[1]+node.u[1]*amp),rc,color="k")
        ax.add_patch(p)

    if fin:
        plt.show()
    else:
        plt.pause(0.001)
