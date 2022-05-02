## readme


**To find the shape/form of a highly geometry nonlinear structre.**

### Checklist before init a new model from SAP2000
- Constrains must be pinned, i.e. Ux, Uy, Uz fixed **ONLY**
- If use special groups for different properties, make sure the group name has been assigned to target frames.
- If do form finding based on selfweight, iteration is needed, and mass source shall be defined in Sap2000. See **eg_double_oval_form_found by dead.py**

### Notes
- If use init_fr_sap, please modify pre-loads and constrains only in SAP2000.
- If initiate a mxn or mx1 model, following steps must be done.
`aaa = TwoDShapeFinding(m, n, 2)
aaa.set_fix(*constrain)
aaa.set_fix([20, 20], [10, 10])
aaa.set_init_F(*loading)
aaa.set_init_z(*boundary_z)
aaa.set_init_z([20, 20, 10], [10, 10, 10])
aaa.set_connectivities()
aaa.set_force_density(10000)
aaa.force_density("g", True,
                  "China", "JTG", "JTGD62 fpk1470", 7, 0.06)`



### Original readme, will be deleted later
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