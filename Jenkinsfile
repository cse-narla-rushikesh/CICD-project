pipeline {
    agent any

    environment {
        DOCKER_USER  = "narlarushikesh"
        DOCKER_REPO  = "narlarushikesh/cicd-project"
        TAG          = "${BUILD_NUMBER}"   // unique tag for every build
        CONTAINER    = "cicd-container"
    }

    stages {

        stage("Checkout Code") {
            steps {
                echo "Checking out latest code from GitHub"
                checkout scm
            }
        }

        stage("Build Docker Image") {
            steps {
                echo "Building fresh Docker image (no cache)"
                bat """
                    docker build --no-cache -t %DOCKER_REPO%:%TAG% .
                """
            }
        }

        stage("Push to Docker Hub") {
            steps {
                echo "Pushing image to Docker Hub"
                withCredentials([usernamePassword(
                    credentialsId: "docker-hub-credentials",
                    usernameVariable: "DOCKER_ID",
                    passwordVariable: "DOCKER_PASS"
                )]) {
                    bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_ID% --password-stdin
                        docker push %DOCKER_REPO%:%TAG%
                    """
                }
            }
        }

        stage("Deploy Container") {
            steps {
                echo "Stopping old container (if exists)"
                bat """
                    docker stop %CONTAINER% || echo No running container
                    docker rm %CONTAINER% || echo No container to remove

                    echo Running new container
                    docker run -d -p 5000:5000 --name %CONTAINER% %DOCKER_REPO%:%TAG%
                """
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline executed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
        always {
            echo "🎬 Build Number: ${BUILD_NUMBER}"
        }
    }
}
