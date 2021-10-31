from setuptools import setup


setup(
        name='arranger',
        version='1.0.0',
        description="moves each file to its appropriate directory based on the fil's extension.",
        author='j0eTheRipper',
        author_email='j0eTheRipper0010@gmail.com',
        url='https://github.com/j0eTheRipper/arranger',
        scripts=['bin/arrange'],
        packages=['engine', 'engine.Extensions', 'engine.File', 'engine.DIR'],
        package_dir={'engine': 'src/engine'},
)
