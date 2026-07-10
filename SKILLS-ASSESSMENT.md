# Skills Assessment — apigee-edge-opdk

| Field | Value |
|-------|-------|
| **Repo** | `apigee-edge-opdk` |
| **Skill domain** | Apigee Edge Private Cloud (OPDK) automation — distributed API-gateway platform operations |
| **Employer context** | Apigee → Google (2015–2016) |
| **Medium** | Ansible, Python custom modules, Jinja2 |

## Expertise demonstrated

This monorepo is the foundational OPDK automation work: ~120 roles that treat a deployment as a **Planet → Region → Pod → Host → Service** hierarchy, derive nearly every operational decision from that graph and the Ansible inventory, and reconcile server state against the Apigee management REST API. The durable expertise is not "Ansible role authoring"; it is the systems-thinking encoded into the framework.

## How this repo shows it

### 1. Distributed-systems operations
- Rolling, `serial:1`, dependency-ordered changes that preserve Cassandra quorum and routing availability.
- Multi-datacenter expansion without taking the planet down — add a second/third region with correct cross-DC Cassandra ring join, Postgres replication, and router re-registration.

### 2. Cassandra cluster administration
- `nodetool rebuild` from a named source DC.
- Ring expansion across DCs.
- Client/data-node package split.
- Registration via the Management Server.

### 3. Postgres HA & Apigee analytics
- Master/standby replication.
- Axgroup/consumer-group/datastore registration.
- Scope binding by `(org, env)`.

### 4. Apigee platform lifecycle
- The `apigee-setup` profile taxonomy.
- Two-phase `install` → `setup -f <response file>` toolchain.
- Silent-install response files dynamically generated from the planet/data-center model.

### 5. Linux systems administration
- Idempotent, proxy-aware OS-prerequisites pipeline: EPEL → iptables → yum → limits → sysctl → SELinux → reboot-gate → OpenJDK.

### 6. Network & port validation
- Per-component internal/external port-connectivity validators with client/server split for cross-node reachability through firewalls.

### 7. AWS provisioning
- `aws-create`/`start`/`stop`/`terminate` lifecycle with the canonical Apigee port matrix.

### 8. Framework architecture
- Object-graph topology model (`Planet → Region → Host → Service`).
- Idempotent REST reconciliation (`/v1/servers/{uuid}`).
- Keystone-role design (`opdk-setup-default-settings` inherited by all roles).

## Why this matters

Most "Ansible automation" is a collection of roles. This is a framework: the inventory is the source of truth, the graph drives every operation, and the API is reconciled idempotently. That same pattern — model the world, derive operations from the model, reconcile idempotently — scales from OPDK to Kubernetes to AI agent infrastructure.

## Related repos

- [`apigee-opdk-playbook-maintenance-opdk-upgrade`](https://github.com/carlosfrias/apigee-opdk-playbook-maintenance-opdk-upgrade/blob/master/SKILLS-ASSESSMENT.md) — two-layer traffic fencing + topology-aware rollback
- [`apigee-opdk-cassandra-rebuild`](https://github.com/carlosfrias/apigee-opdk-cassandra-rebuild/blob/master/SKILLS-ASSESSMENT.md) — Cassandra ring rebuild
- [`apigee-opdk-setup-postgres-failover`](https://github.com/carlosfrias/apigee-opdk-setup-postgres-failover/blob/master/SKILLS-ASSESSMENT.md) — Postgres HA switchover
- [`apigee-hybrid-workspace`](https://github.com/carlosfrias/apigee-hybrid-workspace/blob/master/SKILLS-ASSESSMENT.md) — Kubernetes-native Apigee Hybrid portfolio hub

## Provenance

Authored and maintained by **Carlos Frias** as a Customer Solutions Architect on Apigee Edge Private Cloud. This framework originated as a consolidated monorepo (2015–2016) and was later factored into the modular `apigee-opdk-*` role corpus. The cloud-native successor is [`apigee-hybrid-workspace`](https://github.com/carlosfrias/apigee-hybrid-workspace).