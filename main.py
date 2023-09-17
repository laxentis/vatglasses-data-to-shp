import json
import shapefile
import argparse


def ddmmss_to_int(dms):
    i = 0;
    if len(dms) > 6:
        i = 1;
    d = int(dms[0+i:2+i])
    m = int(dms[2+i:4+i])
    s = int(dms[4+i:6+i])
    return d + m/60 + s/3600


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert VatGlasses Data to ESRI Shapefile")
    parser.add_argument('file', type=str, help="VarGlasses JSON data file")

    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        airspace = data["airspace"]
        filename = args.file.split('.')[0]
        w = shapefile.Writer(filename, shapeType=shapefile.POLYGON)
        w.field('id', 'C')
        w.field('group', 'C')
        w.field('owner', 'C')
        w.field('min', 'N')
        w.field('max', 'N')
        for space in airspace:
            id = space["id"]
            group = space["group"]
            owner = ", ".join(space["owner"])
            for sector in space["sectors"]:
                min = sector["min"]
                max = sector["max"]
                points = []
                for point in sector["points"]:
                    points.append([ddmmss_to_int(point[1]), ddmmss_to_int(point[0])])
                w.poly([points])
                w.record(id, group, owner, min, max)
        w.close()
