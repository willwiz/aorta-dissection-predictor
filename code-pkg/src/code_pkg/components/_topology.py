from typing import TYPE_CHECKING, Literal

from cheartpy.fe.api import (
    create_basis,
    create_boundary_basis,
    create_top_interface,
    create_topology,
)

from ._types import TopologyMap, TopologyType

if TYPE_CHECKING:
    from cheartpy.fe.trait import ICheartTopology

    from code_pkg.mesh import MeshDef


def create_cylinder_topologies(mesh: MeshDef) -> TopologyMap[TopologyType]:
    basis = {k: create_basis(m["elem"], "NL", m["order"]) for k, m in mesh["top"].items()}
    tops: dict[TopologyType, ICheartTopology] = {
        k: create_topology(f"TP{m['prefix']}", basis=basis[k], mesh=mesh["home"] / m["prefix"])
        for k, m in mesh["top"].items()
    }
    interface = create_top_interface("OneToOne", [*tops.values()])
    left = create_topology(
        f"{tops['Disp']}Left",
        basis=create_boundary_basis(basis["Disp"]),
        mesh=mesh["home"] / (mesh["top"]["Disp"]["prefix"] + "_inlet"),
    )
    left.create_in_boundary(tops["Disp"], mesh["bnds"]["Inlet"]["tag"])
    right = create_topology(
        f"{tops['Disp']}Right",
        basis=create_boundary_basis(basis["Disp"]),
        mesh=mesh["home"] / (mesh["top"]["Disp"]["prefix"] + "_outlet"),
    )
    right.create_in_boundary(tops["Disp"], mesh["bnds"]["Outlet"]["tag"])
    tops["Inlet"] = left
    tops["Outlet"] = right
    surfaces: dict[Literal["Inlet", "Outlet"], ICheartTopology] = {
        "Inlet": left,
        "Outlet": right,
    }
    surf_interfaces = [
        create_top_interface(
            "ManyToOne",
            [t],
            master=tops["Disp"],
            interface_file=mesh["home"] / f"iface-{k}.IN",
            nest_in_bnd=mesh["bnds"][k]["tag"],
        )
        for k, t in surfaces.items()
    ]
    return TopologyMap[TopologyType](interface, *surf_interfaces, kwargs=tops)
