"""Views package.

The web application routes which render the pages through CRUD API
methods. The routes are all registered under blueprints utilizing
the Flask extension Flask-Blueprint. The structure allows for a better
organization for the application entrypoints.

After creating a new blueprint, register the blueprint in the
application entrypoint `register_blueprint` function with the code
below::

    app.register_blueprint(module.blueprint)
"""
