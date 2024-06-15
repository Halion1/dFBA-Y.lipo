reaction = Reaction('y300083')
reaction.name = 'Propionate Extracellular Transporter'
reaction.subsystem = 'Cell Propionate Biosynthesis'
reaction.lower_bound = 0. # This is the default
reaction.upper_bound = 1000. # This is the default

propio_extr = Metabolite(
's_3717',
formula='C3H5O2',
name='Propionate[e]',
compartment='e')
propio_c = Metabolite(
's_3718',
formula='C3H5O2',
name='Propionate[c]',
compartment='c')

reaction.add_metabolites({
propio_extr: -1.0,
propio_c: 1.0,
})
reaction.reaction

yali.add_reactions([reaction])

yali.reactions.y300083

propio_c = Metabolite(
's_3718')
propiocoa_c = Metabolite(
's_3719',
formula='C24H36N7O17P3S',
name='Propionyl-CoA[c]',
compartment='c')

reaction1.add_metabolites({
propio_c: -1.0,
propiocoa_c: 1.0,
})
reaction1.reaction

yali.add_reactions([reaction1])

yali.reactions.y300084

