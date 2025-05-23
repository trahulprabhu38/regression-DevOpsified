variable "ami" {
  description = "AMI ID for the EC2 instance."
  type        = string
  default     = "ami-0953476d60561c955"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "docker_image" {
  description = "Docker image for the Streamlit app."
  type        = string
  default     = "trahulprabhu38/mlops:v1"
}

variable "key_name" {
  description = "Key name for the EC2 instance."
  type        = string
  default     = "aws-key"
}
