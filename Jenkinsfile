pipeline {
    agent none
    stages {
        stage('Compile') {
            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {
                sh 'python -m py_compile **.py'
                stash(name: 'compiled-results', includes: '**.py*')
            }
        }
    }
}
