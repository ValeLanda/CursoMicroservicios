pipeline {
    agent {
        node {label 'master'} //Checar en la instalación de Jenkis qué etiquetas tienen los nodos
    }
    environment {
        APPLICATION_NAME = 'api-base-rest'
        GIT_REPO="https://github.com/ixevcorp/api-base/"
        GIT_BRANCH="main"
        GIT_CREDENTIALS="apipoc-git" //este ID se configura cuando se dan de alta las credenciales 
        STAGE_TAG = "promoteToQA"
        DEV_PROJECT = "api-base"
        STAGE_PROJECT = "stage"
        TEMPLATE_NAME = "api-base-buildconfig"//Este template debe existir en Openshift (Builds->BuildConfigs)
                                              //Se crea a partir del Dockerfile, usando el repositorio de GIT
                                              //y se le dan permisos al usuario Jenkins para que lo pueda leer
                                              //$ oc policy add-role-to-user edit system:serviceaccount:jenkins:jenkins -n api-base

        ARTIFACT_FOLDER = "target"
        PORT = 8080;
    }
    stages {
        stage('Get Latest Code') {
            steps {
                git credentialsId: "${GIT_CREDENTIALS}", branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
            }
        }
        stage ("Install Dependencies") {
            steps {
                sh """
                python3 -m venv virtual-env
                source virtual-env/bin/activate
                pip3 install --user -r app/requirements.pip
                deactivate
                """
            }
        }
        /*
        stage('Run Tests') {
            steps {
                sh '''
                source bin/activate
                nosetests app --with-xunit
                deactivate
                '''
                junit "nosetests.xml"
            }
        }
        */
        stage('Store Artifact'){
            steps{
                script{
                    def safeBuildName  = "${APPLICATION_NAME}_${BUILD_NUMBER}",
                        artifactFolder = "${ARTIFACT_FOLDER}",
                        fullFileName   = "${safeBuildName}.tar.gz",
                        applicationZip = "${artifactFolder}/${fullFileName}"
                        applicationDir = ["app",
                                            "config",
                                            "Dockerfile",
                                            ].join(" ");
                    def needTargetPath = !fileExists("${artifactFolder}")
                    if (needTargetPath) {
                        sh "mkdir ${artifactFolder}"
                    }
                    sh "tar -czvf ${applicationZip} ${applicationDir}"
                    archiveArtifacts artifacts: "${applicationZip}", excludes: null, onlyIfSuccessful: true
                }
            }
        }
        stage('Create Image Builder') {
            when {
                expression {
                    openshift.withCluster() {
                        openshift.withProject(DEV_PROJECT) {
                            return !openshift.selector("bc", "${TEMPLATE_NAME}").exists();
                        }
                }
            }
        }
        steps {
            script {
                openshift.withCluster() {
                    openshift.withProject(DEV_PROJECT) {
                        openshift.newBuild("--name=${TEMPLATE_NAME}", "--docker-image=docker.io/nginx:mainline-alpine", "--binary=true")
                        }
                    }
                }
            }
        }
        stage('Build Image') {
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(env.DEV_PROJECT) {
                            openshift.selector("bc", "$TEMPLATE_NAME").startBuild("--from-archive=${ARTIFACT_FOLDER}/${APPLICATION_NAME}_${BUILD_NUMBER}.tar.gz", "--wait=true")
                        }
                    }
                }
            }
        }
        stage('Deploy to DEV') {
            when {
                expression {
                    openshift.withCluster() {
                        openshift.withProject(env.DEV_PROJECT) {
                            return !openshift.selector('dc', "${TEMPLATE_NAME}").exists()
                        }
                    }
                }
            }
            steps {
                script {
                    openshift.withCluster() {
                        openshift.withProject(env.DEV_PROJECT) {
                            def app = openshift.newApp("${TEMPLATE_NAME}:latest")
                            app.narrow("svc").expose("--port=${PORT}");
                            def dc = openshift.selector("dc", "${TEMPLATE_NAME}")
                            while (dc.object().spec.replicas != dc.object().status.availableReplicas) {
                                sleep 10
                            }
                        }
                    }
                }
            }
        }
    }
}
