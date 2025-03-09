{{/*
Expand the name of the chart.
*/}}
{{- define "nocobase.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "nocobase.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "nocobase.dbname" -}}
{{- printf "%s-db" ( include "nocobase.name" .) }}
{{- end }}
{{- define "nocobase.redisname" -}}
{{- printf "%s-redis" ( include "nocobase.name" .) }}
{{- end }}
{{- define "nocobase.servername" -}}
{{- printf "%s-server" ( include "nocobase.name" .) }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "nocobase.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "nocobase.labels" -}}
helm.sh/chart: {{ include "nocobase.chart" . }}
{{ include "nocobase.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "nocobase.selectorLabels" -}}
app.kubernetes.io/name: {{ include "nocobase.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "nocobase.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "nocobase.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
