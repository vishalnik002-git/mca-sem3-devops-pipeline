variable "location" {
  description = "Azure region for deployment"
  type        = string
  default     = "Central India"
}

variable "resource_group_name" {
  description = "Resource Group Name"
  type        = string
  default     = "mca-devops-rg"
}

variable "acr_name" {
  description = "Azure Container Registry Name (alphanumeric only, must be globally unique)"
  type        = string
  default     = "mcadevopsreg2026"
}

variable "app_service_name" {
  description = "Azure Linux Web App Service Name"
  type        = string
  default     = "mca-devops-webapp-2026"
}