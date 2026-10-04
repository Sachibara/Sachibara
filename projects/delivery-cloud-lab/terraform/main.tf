terraform {
  required_version = ">= 1.6, < 2.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 6.0" } }
}
provider "aws" {
  region = var.region
  default_tags { tags = { Project = "SachibaraEngineering", Environment = "lab" } }
}
variable "region" {
  type = string
  default = "ap-southeast-1"
}
variable "bucket_name" {
  type = string
  description = "Globally unique lowercase bucket name for lab artifacts."
  validation {
    condition = can(regex("^[a-z][a-z0-9-]{3,61}[a-z0-9]$", var.bucket_name))
    error_message = "Use 5–63 lowercase letters, digits and hyphens, beginning with a letter."
  }
}
resource "aws_vpc" "lab" {
  cidr_block = "10.60.0.0/16"
  enable_dns_support = true
  enable_dns_hostnames = true
}
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.lab.id
  cidr_block = "10.60.1.0/24"
  map_public_ip_on_launch = false
}
resource "aws_s3_bucket" "artifacts" { bucket = var.bucket_name }
resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
output "private_subnet_id" { value = aws_subnet.private.id }
output "artifact_bucket" { value = aws_s3_bucket.artifacts.id }
