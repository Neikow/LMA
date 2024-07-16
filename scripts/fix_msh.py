import math


def main():
    with open('Meshes/output.msh', 'r') as f:
        lines = f.readlines()

        mult = 10e11

        pts = {}

        inside_nodes = False
        for i in range(len(lines)):
            if lines[i].startswith('$Nodes'):
                inside_nodes = True
                i += 1
                continue

            if lines[i].startswith('$EndNodes'):
                break

            if inside_nodes:
                if lines[i].strip():
                    parts = lines[i].split()
                    if len(parts) != 4:
                        continue

                    pt = (f'{math.floor(float(parts[1]) * mult)}{math.floor(float(parts[2]) * mult)}{math.floor(float(parts[3]) * mult)}')

                    if pt not in pts:
                        pts[pt] = 1
                    else:
                        print(parts[0])
                        pts[pt] += 1


if __name__ == '__main__':
    main()
