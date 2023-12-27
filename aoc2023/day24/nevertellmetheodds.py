import numpy as np 


def falling_hail(filename):
    pos_velocity_noz = []
    vars_xy = []
    sols_xy = []
    vars_xz = []
    sols_xz = []
    x_1, y_1, z_1 = (0, 0, 0)
    dx_1, dy_1, dz_1 = (0, 0, 0)
    with open(filename) as f:
        for i, line in enumerate(f.readlines()):
            pos, veloc = line.split(" @ ")
            initial = [int(p) for p in pos.split(", ")]
            x, y, z = initial
            velocity = [int(v) for v in veloc.split(", ")]
            dx, dy, dz = velocity
            pos_velocity_noz.append((i, dx, dy, x, y))
            if 0 < i < 5:
                vars_xy.append([dy_1 - dy, dx - dx_1, y - y_1, x_1 - x])
                sols_xy.append(x_1 * dy_1 - y_1 * dx_1 - x * dy + y * dx)
                vars_xz.append([dz_1 - dz, dx - dx_1, z - z_1, x_1 - x])
                sols_xz.append(x_1 * dz_1 - z_1 * dx_1 - x * dz + z * dx)
            x_1, y_1, z_1 = initial
            dx_1, dy_1, dz_1 = velocity 
            if i == 4:
                xy = np.linalg.solve(np.array(vars_xy), sols_xy)
                xz = np.linalg.solve(np.array(vars_xz), sols_xz)
                print(xy[0] + xy[1] + xz[1])
        
    paths_crossed = []
    max_up = 400000000000000
    max_down = 200000000000000
    if "example" in filename:
        paths_crossed = get_collided_hail(27, 7, pos_velocity_noz)
    else:
        paths_crossed = get_collided_hail(max_up, max_down, pos_velocity_noz)
    print(len(paths_crossed))
            
    
def get_collided_hail(max_up, max_down, pos_velocity_noz):
    paths_crossed = []
    for i, item in enumerate(pos_velocity_noz):
        hail, dx_i, dy_i, x_i, y_i = item 
        for new_hail in pos_velocity_noz[i + 1:]:
            j, dx_j, dy_j, x_j, y_j = new_hail
            sl_i = dy_i / dx_i 
            sl_j = dy_j / dx_j 
            if sl_i != sl_j:
                x = (x_j * sl_j - x_i * sl_i + y_i - y_j) / (sl_j - sl_i)
                y = sl_i * x - sl_i * x_i + y_i 
                t_i = (x - x_i) / dx_i
                t_j = (x - x_j) / dx_j
                if max_down <= x <= max_up and max_down <= y <= max_up:
                    if t_i > 0 and t_j > 0 :
                        paths_crossed.append((hail, j, t_i, t_j))
    return paths_crossed
    
                