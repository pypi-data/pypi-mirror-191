coverage xml && sonar-scanner.bat -D"sonar.projectKey=jeng" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.login=sqp_e08265acaccfb9234538686b1eb04d32706657dd"

python setup.py sdist bdist_wheel
twine upload .\dist\* --skip-existing