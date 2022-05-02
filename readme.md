## About


**To find the shape/form of a highly geometry nonlinear structre.**

## Checklist 
Before init a new model from SAP2000...
- Constrains must be pinned, i.e. Ux, Uy, Uz fixed **ONLY**
- If use special groups for different properties, make sure the group name has been assigned to target frames.
- If do form finding based on selfweight, iteration is needed, and mass source shall be defined in Sap2000. See [eg double oval form found by dead](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/eg_double_oval_form_found%20by%20dead.py)
## Get Started
### 1. Initiate a MxN 2d web model
Open this file and start to rock!!!  
[eg_2d-pretensioned-net](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/eg_2d-pretensioned-net.py)
- Initiate an instance  
`aaa = TwoDShapeFinding(m, n, 2)`  
    - m is node number in X dir.  
    - n is node number in Y dir.  
    - "2" means node distance is 2.  
        > The unit sys is KN.m.C
- Set constrains  
`aaa.set_fix(*constrain)`  
    - "constrains" is a list of column and row numbers, e.g.  
    `[[0, 0], [2, 4],...]`  
    - To add additional constrains  
    `aaa.set_fix([20, 20], [10, 10]) # optional for additional constrains`  
- Set joint loads  
`aaa.set_init_F(*loading)`  
    - "loading" is a list of column, row and joint force, e.g.  
    `[[0, 0, 1], [2, 4, 10],...]`  
    - Joint load are considered positive in gravity direction.  
    - One can just set initial loads of all 0 by  
    `aaa.set_init_F()`  
- Set bounday conditions  
`aaa.set_init_z(*boundary_z)`  
    - "boundary_z" means to define initial z coords for every points.  
    - One can just set initial Z coords of all 0 by  
    `aaa.set_init_z()`  
    - If you need some points having different z coords, just insert  
    `aaa.set_init_z([20, 20, 10], [10, 10, 10]) # optional for addtional z coords`  
- Set connections  
`aaa.set_connectivities()`  
    - This is must be done.  
- Set frame force densities  
`aaa.set_force_density(10000)`  
    - "10000" is to set all frames force densities of 10000 kN/m
    - When it's postive, means the frame in tension.
    - For special values, just use  
    `aaa.set_force_density(default_rou, [frameID1, rou1], [frameID2, rou2], ..)`  
- Run  
`aaa.force_density("g", True, "China", "JTG", "JTGD62 fpk1470", 7, 0.06)`  
    - 1st parameter, what's to return.  
        - "g" means to return a matplotlib graph.  
        - "w" returns all coords after form finding instead.  
    - 2nd parameter, to bake to Sap2000  
        - True means to return a sap model.  
            > Sap2000 must be opened by hand first.  
            > The rest parameters are for frame properties in Sap2000.  
        - If it is False, no material properties needed.  
        `aaa.force_density("g", False)`  
### 2. Initate a model from Sap2000
> To start, copy an sap model from [here](https://github.com/riverinme/Structure_Form_Finding_HH/tree/master/SAP%20Models) and the relative py.  
> All nodes and frame elements will be used in form finding.  
> The model unit MUST be **kN/m/C**.  
1. Open the model in SAP2000
2. In py, 
    - initiate the instance,  
    `a = TwoDShapeFinding(1, 3, 1, init_fr_sap=True)`
        > m, n, size will be no funtional.  
    - then,  
    `a.init_fr_sap2000("Pre_loading",` 
                      `"China", "JTG", "JTGD62 fpk1470", 7, 0.3, 2000,`  
                      `["inner_up", "China", "JTG", "JTGD62 fpk1470", 7,`  
                      `0.3, 1500],...)`  
        - 1st parameter, pre defined load patterns in Sap2000.
        - 2nd to 5th parameters, Sap2000 material library parameters.
        - 6th parameter, section diameter of the frame object.
            > Use circular rod to simulate everything for now...  
        - 7th parameter, the **frame force density**.  
        >Since sap2000 involved, material properties thus are mandatory.  
        >By using group definition in SAP2000, different materials/force densities are support. Just put group name and other special material properties in [].  
    - Run
    `ll1 = a.force_density("w", False, tolerance=1e-9, remove=False)`  
        > The first 2 parameters are useless.  
        > If 'remove=True', tolerance can be larger, like 1e-4.  
        > FYI, this method can return frame lengths.  
3. If you want to do form finding under structure self weight,  
    > replace `"Pre_loading"` by `mass_assign(a.SapModel, "Pre_loading")`  
    


