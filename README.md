# apigee-edge-opdk — Apigee Edge Private Cloud (OPDK) Automation Framework

> **A framework that models an Apigee planet as an object graph and converges it idempotently** — install, configure, expand, migrate, recover, and tear down distributed API-gateway infrastructure across arbitrarily sized, multi-datacenter topologies.

This is the foundational OPDK automation work: ~120 roles that treat a deployment as a **Planet → Region → Pod → Host → Service** hierarchy, derive nearly every operational decision from that graph and the Ansible inventory, and reconcile server state against the Apigee management REST API. Originally built 2015–2016 for Apigee Edge Private Cloud 15.07 / 16.01 / 16.05 and Apigee BaaS Private Cloud; the approach was later factored into the modular `apigee-opdk-*` role corpus (170+ repositories) for later releases.

## Framework context

This repository is the 2015–2016 origin of the Apigee OPDK Ansible automation framework. The monolithic framework you see here modeled an Apigee planet as an object graph and converged it idempotently via custom Python modules against the Apigee Management Server REST API.

That approach evolved into today's modular `apigee-opdk-*` role corpus — one repository per concern, so each role can be tested, versioned, and reused independently. The modern entry point for the OPDK lifecycle is [`apigee-opdk-playbook-setup-ansible`](https://github.com/carlosfrias/apigee-opdk-playbook-setup-ansible).

For the portfolio view that routes to all skill domains, see the [`apigee-hybrid-workspace` Skills Assessment](https://github.com/carlosfrias/apigee-hybrid-workspace/blob/master/SKILLS-ASSESSMENT.md).

<!-- BEGIN Google Required Disclaimer -->

## Not Google Product Clause

This is not an officially supported Google product.
<!-- END Google Required Disclaimer -->

---

## Why this project is notable

- **A framework, not a role collection.** A keystone role (`opdk-setup-default-settings`) inherited by all roles distributes defaults + a custom Python module library; inventory is the single source of truth for topology.
- **Object-graph topology model.** `apigee_facts.py` models the planet as `Planet → Region → Host → Service` and drives operations from the graph, not hardcoded values.
- **Idempotent REST reconciliation.** Server registration is reconciled against the Apigee Management Server `/v1/servers/{uuid}` API (GET/POST/DELETE) — re-runnable without enrolling duplicates.
- **Dynamically-generated silent-install.** Response files are generated from the planet/data-center model, not checked in.
- **Installs *and* debugs a planet.** The same graph that lays down an installation drives health inspection, port validation, and forensic log/config capture.

---

## What the framework actually does

- **Silent-install response files are dynamically generated** from the planet/data-center model.
- **Server registration is reconciled idempotently** against the Apigee Management Server REST API (`/v1/servers/{uuid}`) so routers, message processors, Qpid, and Postgres nodes are enrolled/deregistered safely and re-runnable.
- **Topology-aware operations** — Cassandra ring rebuilds stream from a named source DC; Postgres master/standby pairs register as a single datastore; analytics axgroups/scopes/consumers are created and torn down in dependency order.
- **Multi-datacenter expansion** — install a region, then add a second/third region with correct cross-DC Cassandra ring join, Postgres replication, and router re-registration, without taking the planet down.
- **Selective rollback** of installed components for troubleshooting, with bootstrap rollback and per-component rollback roles.

---

## Framework architecture

```
opdk-setup-default-settings   ← keystone role: defaults + custom module library, inherited by all roles
└── library/
    ├── apigee_facts.py              ← Planet → Region → Host → Service object-graph model
    ├── opdk_server_registration.py  ← idempotent /v1/servers/{uuid} reconciliation
    ├── opdk_server_self.py          ← node self-introspection (UUID, region, pod)
    ├── zk_connected.py              ← Zookeeper quorum/leader introspection
    ├── bootstrap.py                 ← OPDK bootstrap handling
    ├── cache.py                     ← cross-role fact caching
    └── selinux_status.py            ← SELinux state detection
```

**Why a keystone role?** All OPDK roles declare `opdk-setup-default-settings` as a dependency. Defaults and the module library are distributed from one centralized source while still allowing per-deployment overrides — framework design (separating defaults / library / inventory / composition), not role authoring.

**Why inventory as the source of truth?** DCs, regions, racks, seeds, and roles are derived from Ansible groups (`dc_1`..`dc_n`, `planet`, component groups) rather than hardcoded, so the framework scales with the inventory.

> [!NOTE]
> Engineering portfolio note — this project demonstrates distributed-systems architecture and Apigee platform operations. See the [skills assessment →](SKILLS-ASSESSMENT.md) for the expertise applied.

---

## Capability map

| Group | Roles (selected) | Purpose |
|-------|------------------|---------|
| **Lifecycle / setup** | `opdk-setup-{aio,ds,ms,rmp,router,message-processor,qpid,postgres,ldap,ui,mo,sax,…}` | Per-profile install + configure |
| **Silent install** | `opdk-setup-silent-installation-config`, `opdk-setup-apigee-{property,config,log}-files` | Dynamically generate the silent-install response file + overrides |
| **Migration** | `opdk-migration-{cs,cs-zk,edge,installer,ldap,mo,mp,ms,ps,qpid,qpid-ps,rmp,router,sax,ui,zk}` | Version-to-version migration paths |
| **Cassandra** | `opdk-cassandra-rebuild`, `opdk-cassandra-client-update`, `opdk-migration-cs` | Ring rebuild, client updates, CS migration |
| **Postgres / analytics** | `opdk-setup-{postgres,postgres-master,postgres-standby,sax,sax-replication,sax-replication-{master,slave}}`, `opdk-server-analytics-registration` | Replication + analytics registration |
| **Registration** | `opdk-server-{analytics-registration,deregistration}` | Idempotent MS enrollment/deregistration |
| **Validation** | `internal-port-connectivity-validator-{cassandra,postgres,qpid,mp,router,ms,ldap,ui,zookeeper,baas,baas-elasticsearch,baas-portal}`, `external-port-connectivity-validation-{client,server}` | Cross-node port reachability |
| **Backup / recovery** | `opdk-create-backup`, `opdk-setup-bootstrap-rollback`, `opdk-setup-{component,os,collectd,grafana,graphite}-rollback` | Backup + selective rollback |
| **AWS** | `aws-{create,start,stop,terminate}`, `opdk-setup-aws` | AMI lifecycle |
| **Monitoring** | `opdk-setup-{collectd,grafana,graphite}` | Telemetry stack |
| **BaaS** | `opdk-baas-{create-org-and-user,elasticsearch,setup-component,silent-config-file}`, `opdk-setup-{abp,abs}` | Apigee BaaS (Usergrid) Private Cloud |
| **OS** | `opdk-setup-{os-minimum,os-common,os-ds,os-rmp,os-postgres,os-qpid,os-ldap-downloads,openjdk,selinux-{disable,enable},ssh,time-sync,hostfile}`, `opdk-shutdown-iptables` | OS hardening + prerequisites |
| **Utilities** | `fetch-files`, `restart-node`, `opdk-restart`, `opdk-startup`, `opdk-setup-status`, `opdk-dns-resolver`, `opdk-softlink-prep` | Forensics, restarts, status, DNS |

---

## Sample playbooks

`sample-playbooks/` contains fully functional starter configurations (bring your own inventory):

| Topology | Samples |
|----------|---------|
| 5-node | `5-node-1507-{installation,expansion}`, `5-node-1601-{installation,expansion,migration,migration-archive}`, `5-node-1605-{centos72,installation-ol67,rhel72}` |
| 9-node | `9-node-1507-installation` |
| All-in-one | `aio-node-1507-installation`, `aio-node-1601-{installation,installation-archive}`, `aio-node-1605-installation` |
| Multi-node (16x) | `edge-160x-multi-node-installation` |
| AWS | `aws_management`, `aws-training-env` |
| Vagrant | `vagrant-5node`, `vagrant-7node`, `vagrant-aio` |
| BaaS | `baas-installation` |
| Customer / ops | `tmobile`, `tombstone_fix` (Cassandra tombstone repair) |

---

## Usage

### Conventions

- **`~/.apigee/`** — a hidden folder in your user home holds resources that must not be in source control: license files, download credentials, Ansible encrypted vaults, and binaries.
- **License** — provide your OPDK license file at the path specified by `opdk_license_source_file_name` on the control machine.
- **Binaries** — OPDK binaries are downloaded dynamically. For 15.07.03 you must also provide download credentials.

### Quick start

```bash
ansible-playbook sample-playbooks/<topology>/install.yml -i your_inventory
```

Provide an inventory file matching the planet → region → role group structure (see `sample-playbooks/*/inventory` for starters). Expand to a second region with the corresponding `*-expansion` playbook.

### Supported platforms

CentOS / Oracle Linux / RHEL 6+, on bare metal, AWS, and Vagrant — the roles detect virtualization and adjust accordingly.

### Ansible configuration starter

```ini
[defaults]
gathering = smart
fact_caching = jsonfile
fact_caching_connection = ~/.ansible/facts_cache
fact_caching_timeout = 86400
host_key_checking = False
```

> Persisting the cache to the filesystem helps development. **Do not commit the cache to source control** — it may contain credentials. The `~/.apigee` convention exists to avoid that.

---

## Provenance

Authored and maintained by **Carlos Frias** during his tenure as a Customer Solutions Architect on Apigee Edge Private Cloud. This framework originated as a consolidated monorepo (2015–2016) and was later factored into the modular `apigee-opdk-*` role corpus for later OPDK releases — the cloud-native successor is [`apigee-hybrid-workspace`](https://github.com/carlosfrias/apigee-hybrid-workspace).

## License

See [LICENSE](./LICENSE).