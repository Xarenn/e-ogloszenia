node('docker') {

	stage 'build'
		sh "docker stop nginx"
		sh "docker rm nginx"

	stage 'run'
		sh "docker run --name nginx --hostname nginx -p=5000:80 -d nginx"
}
