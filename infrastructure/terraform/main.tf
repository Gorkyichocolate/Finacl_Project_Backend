terraform {
  required_providers {
    null = {
      source = "hashicorp/null"
    }
  }
}

provider "null" {}

resource "null_resource" "docker_compose_up" {
  provisioner "local-exec" {
    command = "docker compose -f ../../docker-compose.yml up -d --build"
  }
}

resource "null_resource" "docker_compose_down" {
  depends_on = [null_resource.docker_compose_up]

  provisioner "local-exec" {
    when    = destroy
    command = "docker compose -f ../../docker-compose.yml down"
  }
}