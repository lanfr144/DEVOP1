//ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: docker
    image: docker:24.0.7-dind
    command: ['cat']
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-sock
  - name: kubectl
    image: lachlanevenson/k8s-kubectl:v1.27.4
    command: ['cat']
    tty: true
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
'''
        }
    }
    triggers {
        pollSCM('H/2 * * * *')
    }
    stages {
        stage('Pull Code') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Images') {
            steps {
                container('docker') {
                    sh 'docker build -t devop1-backend:latest ./app/backend'
                }
            }
        }
        stage('Run Tests') {
            steps {
                sh 'echo "Running unit and integration tests..."'
            }
        }
        stage('Deploy to Kubernetes') {
            when {
                branch 'production'
            }
            steps {
                container('kubectl') {
                    sh 'kubectl apply -f kubernetes/manifests/'
                }
            }
        }
    }
}