# CloudForge — Kubernetes Delivery Platform

A containerized Flask application deployed three ways to demonstrate
progressive understanding of Kubernetes delivery: raw manifests, Helm,
and managed EKS.

The application is deliberately simple. The **platform** is the project.

## What this repo demonstrates

| Phase | What it shows | Key evidence |
|---|---|---|
| [Phase 1 — Manifests](./phase-1-manifests/) | Deploying to K8s with hand-written YAML, and operating it | [Failure drills](./phase-1-manifests/FAILURE-DRILLS.md) |
| [Phase 2 — Helm](./phase-2-helm/) | Packaging the same app as a reusable chart, with release management | `helm history` showing upgrade + rollback |
| [Phase 3 — EKS](./phase-3-eks/) | Running the same chart on AWS's managed Kubernetes | (in progress) |

## The application

A small Flask service with `/health`, `/api/info`, and a landing page.
Built as a multi-stage Docker image running as non-root.

- Image: `power2020/cloudforge-app:dev`
- Endpoints: `/`, `/health`, `/api/info`, `/api/work`
- Tests: `pytest`

## Architecture

(insert the diagram once Phase 3 exists)

- **Phase 1:** single-node kubeadm cluster on EC2, Calico CNI, NodePort Service
- **Phase 2:** the same cluster, app packaged as a Helm chart
- **Phase 3:** EKS managed control plane, AWS Load Balancer Controller, (TBD)

## Why three phases

Each phase adds a different layer of understanding:

1. **Manifests** — what every K8s object is, why it exists, how to debug it when it breaks
2. **Helm** — how to make deployments repeatable and reversible without copy-paste
3. **EKS** — how managed Kubernetes differs from self-managed, and how cloud infrastructure integrates

The same application runs in all three. Only the delivery mechanism changes.

## Quick start (Phase 1 — fastest to reproduce)

```bash
git clone https://github.com/<you>/cloudforge-k8s-platform.git
cd cloudforge-k8s-platform
kubectl apply -f phase-1-manifests/
kubectl get pods -n cloudforge -w


## Per-phase `README.md`

Each phase directory gets its own README. Structure them the same way:

**`phase-1-manifests/README.md`:**

```markdown
# Phase 1 — Kubernetes manifests from scratch

Goal: deploy the CloudForge app to a kubeadm cluster using hand-written
YAML, one object at a time, and understand every field.

## Cluster setup

(short paragraph: kubeadm on Ubuntu EC2, Calico, untainted control-plane)

Commands used:
```bash
sudo kubeadm init --config kubeadm-config.yaml
kubectl apply -f https://.../calico.yaml
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
kubectl get all -n cloudforge
kubectl describe pod <pod> -n cloudforge
kubectl logs <pod> -n cloudforge
kubectl rollout undo deployment/cloudforge -n cloudforge
kubectl rollout status deployment/cloudforge -n cloudforge


**`phase-2-helm/README.md`:**

```markdown
# Phase 2 — The same app, packaged with Helm

Goal: convert Phase 1's manifests into a reusable Helm chart, and
demonstrate release management (upgrade + rollback).

## Chart layout
cloudforge/
├── Chart.yaml
├── values.yaml
└── templates/
├── _helpers.tpl
├── configmap.yaml
├── secret.yaml
├── deployment.yaml
└── service.yaml


## Install

```bash
cd phase-2-helm/cloudforge
helm install cloudforge . -n cloudforge --create-namespace
helm upgrade cloudforge . -n cloudforge

rollback :-
helm history cloudforge -n cloudforge
helm rollback cloudforge <revision> -n cloudforge


**`phase-3-eks/README.md`** — leave a stub for now:

```markdown
# Phase 3 — Deploying to EKS

(in progress)

Goal: run the same Helm chart on AWS's managed Kubernetes.

Approach: eksctl vs Terraform (decision pending).
