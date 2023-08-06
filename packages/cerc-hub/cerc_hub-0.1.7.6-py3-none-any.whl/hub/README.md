# Hub

Hub is part of Insel4Cities architecture for urban simulations, created by the CERC group at Concordia University.

Hub repository contains:
* city_model_structure: a central data model specifically design to model urban environments. An instance of this is called City.
* catalog_factories: a set of classes to describe catalog structures used by the import and export factories.
* imports: factories to import data from different formats to feed the city model structure (and create a City) or the catalog structures depending on the purpose.
* exports: factories to export desired parts of the City to different formats depending on the purpose, or to export catalogs in a common format.
* data: contains offered data, either for geometry, weather or different types of catalogs.
* other folders to support manipulating data.

Released under [LGPL license](LICENSE.md), will provide an object-oriented, modular approach to urban simulations.

Our aims are: 

* involve as many scientists and contributors as possible.
* provide a complete set of classes that help scientists and students to model urban environments.

Please check the [contributing information](CONTRIBUTING_EXTERNALS.md) and [code of conduct](CODE_OF_CONDUCT.md) if you want to contribute, and let us know any new feature you may be of interest for you or your team.
