terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~>3.0.1"
    }
  }
}


provider "docker" {}

resource "docker_network" "matrix_network" {
    name = "matrix_net"
    ipam_config {
        subnet = "172.15.0.0/24"
    }

}

resource "docker_volume" "psql_volume" {
  name = "pgqldata"
}

resource "docker_image" "postgres_image" {
  name = "postgres:16.0-alpine"
}

resource "docker_container" "postgres_container" {
  name  = "graphql_postgres"
  image = docker_image.postgres_image.name
  
  restart = "unless-stopped"

  env = [
    "POSTGRES_USER=${var.POSTGRES_USER}",
    "POSTGRES_DB=${var.POSTGRES_DB}",
    "POSTGRES_PASSWORD=${var.POSTGRES_PASSWORD}",
  ]

  ports {
    internal = 5432
    external = 5434
  }

  volumes {
    volume_name    = docker_volume.psql_volume.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = docker_network.matrix_network.name
    ipv4_address = "172.15.0.10"
  }
}