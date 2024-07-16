import argparse
import h5py
import os

def main():
    parser = argparse.ArgumentParser(description='Read sensors')
    parser.add_argument('folder', type=str, help='Folder containing the sensors data')
    parser.add_argument('output_file', type=str, help='Output file')
    args = parser.parse_args()
    print(f"Reading folder {args.folder} for sensor data")
    files = os.listdir(os.path.join(args.folder))
    files = [f for f in files if f.endswith('.h5')]

    if not len(files):
        print("No sensor data found")
        exit(1)

    print(files)


if __name__ == '__main__':
    main()
