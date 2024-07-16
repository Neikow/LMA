import argparse


def get_side_name(x: int, y: int, z: int):
    side_name = []
    if x == -1:
        side_name.append('x-')
    elif x == 1:
        side_name.append('x+')

    if y == -1:
        side_name.append('y-')
    elif y == 1:
        side_name.append('y+')

    if z == -1:
        side_name.append('z-')
    elif z == 1:
        side_name.append('z+')

    return ','.join(side_name)


def create_sides_dict(sides_to_create_list: list[str]):
    def should_create(side_name: str):
        for _s in side_name.split(','):
            if _s not in sides_to_create_list:
                return False

        return True

    sides = {}

    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                if x == 0 and y == 0 and z == 0:
                    continue
                side_name = get_side_name(x, y, z)
                sides[side_name] = should_create(side_name)

    return sides


def get_side_normal(side: str, min: float, max: float, thickness: float):
    if side.endswith('+'):
        return f'{max:.8f} {thickness:.8f}'
    else:
        return f'{min:.8f} {thickness:.8f}'


def main():
    parser = argparse.ArgumentParser(description='Create Perfect Match Layers (PML) materials')
    parser.add_argument('output_file', type=str, help='Output file')
    parser.add_argument('-n', type=int, dest='n', help='Number of default materials to create', default=1)
    parser.add_argument('-vp', type=float, dest='vp', help='Default material P wave velocity (in m/s)', default=6400)
    parser.add_argument('-vs', type=float, dest='vs', help='Default material S wave velocity (in m/s)', default=3200)
    parser.add_argument('-d', type=float, dest='d', help='Default material density (in kg/m^3)', default=2700)
    parser.add_argument('-T', type=str, dest='type', help='Default material type (S = solid, F = fluid, ...)', default='S')
    parser.add_argument('-Np',  type=int, dest='npow', help='PML exponential attenuation', default=2)
    parser.add_argument('-A', type=float, dest='A', help='PML exponential coefficient', default=10)
    parser.add_argument('-t', type=float, dest='thickness', help='PML thickness (in m)', default=1)
    parser.add_argument('-xMin', type=float, dest='xmin', help='Minimum distance on the x-axis (in m)', default=0)
    parser.add_argument('-xMax', type=float, dest='xmax', help='Minimum distance on the x-axis (in m)', default=1)
    parser.add_argument('-yMin', type=float, dest='ymin', help='Minimum distance on the y-axis (in m)', default=0)
    parser.add_argument('-yMax', type=float, dest='ymax', help='Minimum distance on the y-axis (in m)', default=1)
    parser.add_argument('-zMin', type=float, dest='zmin', help='Minimum distance on the z-axis (in m)', default=0)
    parser.add_argument('-zMax', type=float, dest='zmax', help='Minimum distance on the z-axis (in m)', default=1)
    parser.add_argument('-s', type=str, dest='sides',
                        help='Sides to create (defaults to all sides besides the top )',
                        default='x+,x-,y+,y-,z-')
    parser.add_argument('-noComments', action='store_true', dest='no_comments', help='Do not create descriptive comments')

    args = parser.parse_args()
    print(f"Creating materials in file {args.output_file}")

    min_max_map = {
        'x': (args.xmin, args.xmax),
        'y': (args.ymin, args.ymax),
        'z': (args.zmin, args.zmax)
    }

    with open(args.output_file, 'w+') as f:
        sides_to_create = create_sides_dict(args.sides.split(','))

        if not args.no_comments:
            f.write(f'# ======================\n')
            f.write(f'#       Materials\n')
            f.write(f'# ======================\n')
            f.write(f'\n')
            f.write(f'# Material count:\n')

        f.write(f'{args.n}\n')

        if not args.no_comments:
            f.write(f'\n')

            f.write(f'# Material properties:\n')
            f.write(f'# type | vel_p | vel_s | dens | q_p | q_s\n')
            f.write(f'\n')
        for i in range(args.n):
            if not args.no_comments:
                f.write(f'# Material {i + 1}\n')

            f.write(f'{args.type} {args.vp:.8f} {args.vs:.8f} {args.d:.8f} {0:.8f} {0:.8f}\n')

            if not args.no_comments:
                f.write(f'\n')

        if not args.no_comments:
            f.write(f'# ======================\n')
            f.write(f'#  Perfect Match Layers\n')
            f.write(f'# ======================\n')
            f.write(f'\n')

            f.write(f'# Perfect Match Layers properties:\n')
            f.write(f'# npow | Apow | posX | widthX | posY | widthY | posZ | widthZ | mat\n')
            f.write(f'\n')

        count = 1
        for side_name, create in sides_to_create.items():
            if not create:
                continue

            if not args.no_comments:
                f.write(f'# PML {count} ({side_name})\n')

            f.write(f'{args.npow} {args.A:.8f} ')

            for axis in ['x', 'y', 'z']:
                if axis in side_name:
                    f.write(get_side_normal(axis + side_name[side_name.index(axis)+1], min_max_map[axis][0], min_max_map[axis][1], args.thickness))
                else:
                    # writes 0 0
                    f.write(get_side_normal('x+', 0, 0, 0))
                f.write(' ')

            f.write(f'0\n')
            if not args.no_comments:
                f.write(f'\n')
            count += 1


if __name__ == '__main__':
    main()
