# Fabric lakehouse ingestion

PySpark notebooks that ingest public California healthcare workforce datasets into a Fabric lakehouse.

This portfolio copy demonstrates architecture and implementation using sanitized
configuration. Infrastructure names and Fabric identities are illustrative.
Source Git history, credentials, local settings and data extracts are not included.
Azure Pipelines YAML is provided as a reference; it needs your own Azure DevOps
project, repository resources, targets and service connections to run.

## Portfolio projects

- [data-acquisition](https://github.com/gainesjw/data-acquisition): A Python collector with managed identity, tested storage writes, and verified Azure Functions releases.
- [platform-dev](https://github.com/gainesjw/platform-dev): Reusable Azure Pipelines templates and Python tooling for immutable releases, dependency validation, and selective Fabric deployment.
- [analytics-dev](https://github.com/gainesjw/analytics-dev): A source-controlled Power BI semantic model and report with environment-aware lakehouse bindings.
- [data-engineering-dev](https://github.com/gainesjw/data-engineering-dev): PySpark notebooks that ingest public California healthcare workforce datasets into a Fabric lakehouse.
- [policy-engine-dev](https://github.com/gainesjw/policy-engine-dev): An ASP.NET Core API returning complete artifact manifests and per-item governance findings for pipeline enforcement.

## Implementation guide

# Data engineering development

Fabric lakehouse and ingestion notebooks under `lakehouse.Lakehouse/` and `etl_notebooks/`, with separate Azure DevOps CI and CD pipelines
consuming the Fabric template family in `platform-dev`. Azure Function App templates
and runtime dependencies are independent.

## CI/CD

| Pipeline | Entry point | Purpose |
| --- | --- | --- |
| `data-engineering-dev-ci` | `.azure-pipelines/ci.yml` | Validate items, generate governance manifest/dependency graph, publish `fabric-release` |
| `data-engineering-dev-cd` | `.azure-pipelines/cd.yml` | Promote the same successful main CI artifact through dev → test → prod |

CI needs no Fabric credentials. Each promotion verifies the upstream run,
artifact hashes and provenance, validates target bindings, publishes items and
records their deployed IDs. A failed or skipped predecessor blocks the next
environment. Test/prod approvals and exclusive locks must be configured on the
Azure DevOps environments; YAML alone does not create these checks.

## Configuration and activation

1. Publish the platform templates before these consumer pipeline changes.
2. Fill dev/test/prod workspace GUIDs in [`.fabric/config.json`](.fabric/config.json).
3. Replace service connection placeholders in [`.azure-pipelines/cd.yml`](.azure-pipelines/cd.yml).
4. Create the named DevOps environments, configure approvals/branch control and
   exclusive locks, grant resource access, and register the two pipelines above.
5. Add main branch build validation in Azure Repos. Run CI and review its artifact
   before enabling CD. Keep CI/CD on the same tested platform reference.

Workspaces and connections are not ready yet. CI is usable with placeholders;
deployment rejects incomplete configuration before publishing. Never put credentials
in configuration. Follow the shared [Fabric setup and operating guide](../platform-dev/docs/fabric/README.md)
in the sibling checkout, or `platform-dev/docs/fabric/README.md` in Azure Repos, for
permissions, registration, approvals, retention and rollback instructions.

Notebook default and known lakehouse IDs are rebound to the lakehouse in the
target environment. `sourceWorkspaceId` records the existing notebook export's
origin; it is not a deployment target. Update it when the authoritative export
workspace changes. Target dev/test/prod IDs intentionally remain placeholders.

The generated graph contains the lakehouse and its three dependent ingestion
notebooks. Deploy this repository before analytics in each environment. Deployment
does not execute notebooks or move lakehouse tables/data between workspaces.

## Automatic item management and governance

[`.fabric/config.json`](.fabric/config.json) defines managed roots, allowed types,
owner/classification defaults, per-logical-ID overrides and external dependencies.
New item folders with valid `.platform` metadata under managed roots are discovered
automatically. Duplicate identities, missing definitions, unresolved supported
references and dependency cycles fail CI. Classification defaults to `internal`
and owner to this repository pending review; this metadata does not apply Fabric
sensitivity labels or grant permissions.

Every CI artifact contains `inventory/manifest.json`, `dependencies.json`, and
Mermaid `dependencies.mmd`/`README.md`, including item file hashes and deployment
order. CD adds environment receipts with physical item IDs and the release digest.
Generated files are not committed back by CI. To inspect them locally:

```bash
PYTHONPATH=../platform-dev/python python3 -m platform_fabric inventory \
  --root . --output .fabric/generated
```

The graph describes supported static deployment dependencies, not complete runtime
or column lineage. Managed definitions are published without deleting orphaned or
unmanaged items. Renames/removals require separately reviewed retirement. External
credentials, data quality checks, model refresh and notebook execution remain
operational setup steps. A failed deployment can leave partial changes; later
promotion stops, and no automatic rollback is attempted.
