import Model as M



Model = M.Model() 

Model.df = 0.35e-2
Model.res = 10/1.55  # at least 10 px per wavelength
Model.Courant = 1


Model.GAP = 1000
Model.BackgroundN = 1.445
Model.N1 = 1.41
Model.N2 = Model.N1

Model.filename = '1D_Test'
Model.Datafile = 'Wooooo'


Model.RunTRspectrum()

