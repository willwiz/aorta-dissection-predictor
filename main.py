from code_pkg.mesh import export_cylinder_mesh, make_cylinder_mesh

from data.mesh import DEFAULT_CYLINDER


def main() -> None:
    mesh, fields = make_cylinder_mesh(
        DEFAULT_CYLINDER["geo"], quad=(DEFAULT_CYLINDER["order"] == 2)
    )
    export_cylinder_mesh(DEFAULT_CYLINDER, mesh, fields)


if __name__ == "__main__":
    main()
