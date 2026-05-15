from pathlib import Path

from cheartpy.paraview.api import cheart2vtu_find

if __name__ == "__main__":
    # cheart2vtu_find(
    #     mesh=Path("mesh_mia/model"),
    #     input_dir=Path("results_release_mia_forward"),
    #     output_dir=Path("results_release_mia_forward"),
    #     var=["U", "P"],
    #     thread=16,
    # )
    # cheart2vtu_find(
    #     mesh=Path("mesh_mia/model"),
    #     input_dir=Path("results_free_mia_inverse"),
    #     output_dir=Path("results_free_mia_inverse"),
    #     var=["U", "P"],
    #     thread=16,
    # )
    # folder = Path("results_aorta_inverse")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=16,
    # )
    # folder = Path("results_straight_inverse")
    # cheart2vtu_find(
    #     mesh=Path("mesh/quad"),
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U"],
    #     thread=16,
    # )
    # folder = Path("results_straight_center")
    # cheart2vtu_find(
    #     mesh=Path("mesh/quad"),
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U"],
    #     thread=16,
    # )
    # folder = Path("results_aorta_inverse")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=16,
    # )
    # folder = Path("results_aorta_detether")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     space=folder / "X0-100.D",
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=16,
    # )
    # folder = Path("results_aorta_forward")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=32,
    # )
    # folder = Path("results_aorta_dettach")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     space=folder / "X0-100.D",
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=32,
    # )
    # folder = Path("results_circ_dettach")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     space=folder / "X0-100.D",
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=32,
    # )
    # folder = Path("results_iso_dettach")
    # cheart2vtu_find(
    #     mesh=Path("mesh_aorta/Lin"),
    #     space=folder / "X0-100.D",
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=32,
    # )
    folder = Path("results_plane_destretch")
    cheart2vtu_find(
        mesh=Path("mesh_plane/Lin"),
        space=folder / "X0-100.D",
        input_dir=folder,
        output_dir=folder,
        var=["U", "P"],
        thread=32,
    )
    # folder = Path("results_plane_inverse")
    # cheart2vtu_find(
    #     mesh=Path("mesh_plane/Lin"),
    #     input_dir=folder,
    #     output_dir=folder,
    #     var=["U", "P"],
    #     thread=16,
    # )
    # cheart2vtu_find(
    #     mesh=Path("mesh_mia/model_quad"),
    #     input_dir=Path("results_release_mia_back"),
    #     output_dir=Path("results_release_mia_back"),
    #     var=["U"],
    #     thread=5,
    # )
    # cheart2vtu_find(
    #     mesh=Path("mesh_mia/model_quad"),
    #     output_dir=Path("results_residual"),
    #     prefix="ResU",
    #     subindex="auto",
    #     var=["U"],
    #     thread=12,
    # )
    # cheart2vtu_find(
    #     mesh=Path("mesh_mia/model"),
    #     output_dir=Path("results_residual"),
    #     prefix="ResP",
    #     subindex="auto",
    #     var=["P"],
    #     thread=12,
    # )
    # cheart2vtu_find(
    #     mesh=Path("mesh_mia/model_outlet"),
    #     output_dir=Path("results_residual"),
    #     prefix="ResLM",
    #     subindex="auto",
    #     var=["TLMOutlet"],
    #     thread=12,
    # )
