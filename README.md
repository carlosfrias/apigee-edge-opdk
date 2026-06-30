# apigee-edge-opdk — Apigee Edge Private Cloud (OPDK) Automation Framework

> A framework for modeling an Apigee **planet** as an object graph and converging it idempotently — install, configure, expand, migrate, recover, and tear down distributed API-gateway infrastructure across arbitrarily sized, multi-datacenter topologies.

This is **not a collection of Ansible roles** — it is a framework. Ansible is the execution medium; the durable work is the **domain model**, the **custom modules** that reconcile state against the Apigee management REST API, and the **sequencing logic** that keeps a distributed stateful system available while it is being changed.

Originally built 2015–2016 to automate Apigee Edge Private Cloud (OPDK) 15.07 / 16.01 / 16.05 and Apigee BaaS Private Cloud. The approach was subsequently decomposed into the modular `apigee-opdk-*` role corpus (175+ repositories) for OPDK 4.16 / 4.17 / 4.19 and beyond.

---

## What the framework actually does

It treats a deployment as a **Planet → Region → Pod → Host → Service** hierarchy (see `opdk-setup-default-settings/library/apigee_facts.py`) and derives nearly every operational decision from that graph and the Ansible inventory, rather than from hardcoded values:

- **Silent-install response files are dynamically generated** from the planet/data-center model — not checked in.
- **Server registration is reconciled idempotently** against the Apigee Management Server REST API (`/v1/servers/{uuid}` GET/POST/DELETE) so routers, message processors, Qpid, and Postgres nodes are enrolled/deregistered safely and re-runnable.
- **Topology-aware operations** — Cassandra ring rebuilds stream from a named source DC; Postgres master/standby pairs are registered as a single datastore; analytics axgroups/scopes/consumers are created and torn down in dependency order.
- **Multi-datacenter expansion** — install a region, then add a second/third region with correct cross-DC Cassandra ring join, Postgres replication, and router re-registration, without taking the planet down.
- **Selective rollback** of installed components for troubleshooting, with bootstrap rollback and per-component rollback roles.

The framework installs **and** debugs a planet: the same graph that lays down an installation also drives health inspection, port validation, and forensic log/config capture.

---

## The underlying expertise demonstrated

> Ansible is the medium. The skills below are what the code actually applies. This section exists so reviewers can evaluate the engineering, not the tool.

| Domain | What's encoded in the code |
|--------|----------------------------|
| **Distributed-systems operations** | Rolling, `serial:1`, dependency-ordered changes that preserve Cassandra quorum and routing availability; traffic drain via the Management Server `reachable` flag. |
| **Cassandra cluster administration** | `nodetool rebuild` from a named source DC, ring expansion across DCs, client/data-node package split, `apigee-service … update`, registration via the MS, CWC override propagation. |
| **Postgres HA & Apigee analytics** | Master/standby replication setup, analytics axgroup/consumer-group/datastore registration, scope binding by (org, env). |
| **Apigee platform lifecycle** | The `apigee-setup` profile taxonomy (`ms`/`r`/`mp`/`rmp`/`qs`/`ps`/`ds`/`ldap`/`ui`/`aio`/`mo`/`baas`), two-phase `install` → `setup -f <response file>`, the `apigee-service`/`apigee-all`/`apigee-provision` toolchain. |
| **Linux systems administration** | OS prerequisites pipeline (EPEL → iptables → yum → limits → sysctl → SELinux → reboot-gate → OpenJDK), idempotent and proxy-aware. |
| **Network & port validation** | Per-component internal/external port-connectivity validators (Cassandra, Postgres, Qpid, MP, Router, MS, LDAP, UI, Zookeeper) with client/server split for cross-node reachability testing through firewalls. |
| **AWS provisioning** | `aws-create`/`-start`/`-stop`/`-terminate` lifecycle for AMI instances, with the canonical Apigee port matrix. |
| **Framework architecture** | A keystone role (`opdk-setup-default-settings`) inherited by all roles distributes defaults and the custom module library; inventory is the single source of truth for topology. |

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

**Why a keystone role?** All OPDK roles declare `opdk-setup-default-settings` as a dependency. Defaults and the module library are distributed from one centralized source while still allowing per-deployment overrides. This is framework design (separating defaults / library / inventory / composition), not role authorship.

**Why inventory as the source of truth?** DCs, regions, racks, seeds, and roles are derived from Ansible groups (`dc_1`..`dc_n`, `planet`, component groups) rather than hardcoded, so the framework scales with the inventory.

---

## Capability map

| Group | Roles (selected) | Purpose |
|-------|------------------|---------|
| **Lifecycle / setup** | `opdk-setup-{aio,ds,ms,rmp,router,message-processor,qpid,postgres,ldap,ui,mo,sax,…}` | Per-profile install + configure |
| **Silent install** | `opdk-setup-silent-installation-config`, `opdk-setup-apigee-{property,config,log}-files` | Dynamically generate the silent-install response file and property overrides |
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

`sample-playbooks/` contains fully functional starter configurations. Bring your own inventory.

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

- **`~/.apigee/`** — a hidden folder in your user home holds resources that must not be in source control: license files, download credentials, Ansible encrypted vaults, and binaries. The starter `ansible.cfg` assumes this.
- **License** — you must provide your OPDK license file at the path specified by `opdk_license_source_file_name` on the control machine.
- **Binaries** — OPDK binaries are downloaded dynamically. For 15.07.03 you must also provide download credentials.

### Quick start

1. Install the keystone + controller:
   ```bash
   ansible-playbook sample-playbooks/<topology>/install.yml -i your_inventory
   ```
2. Provide your own inventory file matching the planet → region → role group structure (see `sample-playbooks/*/inventory` for starters).
3. Expand to a second region with the corresponding `*-expansion` playbook.

### Supported platforms

CentOS / Oracle Linux / RHEL 6+, on bare metal, AWS, and Vagrant — the roles detect virtualization and adjust accordingly.

---

## Ansible configuration starter

Ansible uses an in-memory cache by default. The starter below persists the cache to the filesystem so you can inspect values during development. **Do not commit the cache to source control** — it may contain credentials.

```ini
[defaults]
# Cache to filesystem for development inspectability
gathering = smart
fact_caching = jsonfile
fact_caching_connection = ~/.ansible/facts_cache
fact_caching_timeout = 86400
host_key_checking = False
```

> The `~/.apigee` convention exists to avoid an inadvertent security event: a cache committed to source control could expose credentials.

---

## Provenance

Built and maintained by **Carlos Frias** during his tenure as a Customer Solutions Architect on Apigee Edge Private Cloud. The framework originated as a consolidated monorepo (2015–2016) and was later factored into the modular `apigee-opdk-*` role corpus for later OPDK releases. See the author's profile for the broader Apigee Hybrid / Apigee X / Anthos work that succeeded this era.

## License

See [LICENSE](./LICENSE).