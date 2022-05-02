## About


**To find the shape/form of a highly geometry nonlinear structre.**

## Checklist before init a new model from SAP2000
- Constrains must be pinned, i.e. Ux, Uy, Uz fixed **ONLY**
- If use special groups for different properties, make sure the group name has been assigned to target frames.
- If do form finding based on selfweight, iteration is needed, and mass source shall be defined in Sap2000. See [](eg_double_oval_form_found by dead.py)

## Notes
- If use init_fr_sap, please modify pre-loads and constrains only in SAP2000.  
- If initiate a mxn or mx1 model, following steps must be done.  


## Get started
1. Initiate a MxN 2d web model
- Initiate an instance  
`aaa = TwoDShapeFinding(m, n, 2)`  
    - m is node number in X dir.  
    - n is node number in Y dir.  
    - "2" means node distance is 2.  
      
    > The unit sys is KN.m.C
    
- Set constrains  
`aaa.set_fix(*constrain)`  
    - "constrains" is a list of column and row numbers,i.g. e.g. 
    `[[0, 0], [2, 4],...]`  
    - To add additional constrains
    `aaa.set_fix([20, 20], [10, 10]) # optional for additional constrains`  
    
- Set joint loads  
`# "loading" is a list of column, row and joint force,e.g. e.g. [[0, 0, 1], [2, 4, 10],...]``  
`# Joint load are considered positive in gravity direction`
`aaa.set_init_F(*loading)`  
- Set bounday conditions  
`# "boundary_z" means to define initial z coords of every points.`  
`aaa.set_init_z(*boundary_z)`  
`aaa.set_init_z([20, 20, 10], [10, 10, 10]) # optional for addtional z coords`  
`# One can just set initial load and z coords 0 by aaa.set_init_F() and aaa.set_init_z()`  
- Set connections  
`aaa.set_connectivities() # must be done to get connections of nodes to each other.`
- Set frame force densities  
`# instance.set_force_density(default_rou, [frameID1, rou1], [frameID2, rou2], ..)`  
`# "default_rou is mandatory, special frame force density is optional`
`aaa.set_force_density(10000)`  
- Run  
`# "g" means to return a matplotlib graph. "w" returns all coords after form finding`  
`# True means to return a sap model. Sap2000 must be open by hand first.`  
`# If it is False, no material properties needed.`
`aaa.force_density("g", True, "China", "JTG", "JTGD62 fpk1470", 7, 0.06)`  



## Original readme, will be deleted later
Here is one example.

![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/Eg2.png)

Here is how it looks in SAP2000 with a external point load assigned,
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/unit_point_load.png)

...and the initial deformation under pre-stressing.
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/pre_deformation.png)

The deformation under the point load is shown below， 
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/unit_deformation_NL.png)

...and the load case defination.
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/Unit_NL_case.png)

If the pre case is fogotten, the deformation will increase like
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/unit_deformation_wo_pre.png)

To wrap up, the found geometry and pre-loading(prestressing and/or selfweight) shall be both included in the model. 

### Update 20220427

Here is one example of igloo
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/igloo.png)
![](https://github.com/riverinme/Structure_Form_Finding_HH/blob/master/Eg2/igloo_axial_forces.png)