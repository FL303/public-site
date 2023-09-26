+++
title="Infrastructure Orchestration"
url="/core-components/infrastructure-orchestration"
weight=20
+++

# Infrastructure Orchestration

{{< hint info >}}
TLDR; An Internal Developer Platform (IDP) is the sum of the tech and tools that an Ops, DevOps or platform engineering team glues together to build golden paths for developers. All the existing tools and infrastructure are part of the IDP, they integrate with it and they are orchestrated by the IDP to enable Continuous Delivery or even Continuous Deployment (CD) processes.
{{< /hint >}}

An Internal Developer Platform should always follow a Platform as a Product approach. This is especially important when you cannot build an Internal Developer Platform green field, but need to put it into an existing setup. An Internal Developer Platform typically integrates with your existing CI pipelines on the one side and your hardware infrastructure (e.g. Kubernetes clusters, databases, file storage) on the other side. This is also one of the big differences to PaaS (Platform-as-a-Service) solutions, which typically also includes all the infrastructure (very often based on proprietary technology stacks) out of the box.

The following picture provides a good overview of the typical integration points of an Internal Developer Platform:
{{< figure link="/_assets/images/infrastructure-orchestration.png" src="/_assets/images/infrastructure-orchestration.png" caption="Typical integration points of an Internal Developer Platform" alt="Typical integration points of an Internal Developer Platform" >}}

## Integration points

This section provides an overview of the most important integration points for an Internal Developer Platform. When building an Internal Developer Platform, you should make sure that it (a) provides as many integrations to cover your current setup as possible and (b) allows you to write your own integrations in case you need to do so.

### CI pipelines

Setting up and configuring Continuous Integration (CI) pipelines can be a lengthy process. Once they are set up, you should ideally not touch them unless you really need to. Existing CI pipelines are an essential part of your Internal Developer Platform.

### Clusters

Computer clusters (e.g., Kubernetes clusters) are an important element to run your containerized setup. An Internal Developer Platform should integrate with your existing clusters to run deployments of applications and environments. Ideally, you want to control access via a service account that you can always remove if necessary.

### DNS

Enabling developers and teams to create new environments whenever needed (see also [Environment Management]({{< relref "environment-management" >}})) is an important component of an Internal Developer Platform. Providing environments on demand typically also includes being able to issue new subdomains for the specific environment. An Internal Developer Platform should thus be integrated with your DNS provider to enable this functionality.

### Other resources

There are many more resources relevant for your specific applications. These resources can either run in your cluster (_in-cluster resources_) - typical examples are messaging queues or caching databases - or outside of your cluster (_out-of-cluster resources_) - typical examples include databases and persistent file storage. An Internal Developer Platform ideally allows for an out-of-the-box or at least simple integration of all this infrastructure (including the very specific legacy infrastructure that you just cannot get rid of easily).

### IaC

An Internal Developer Platform ideally integrates well with an existing Infrastructure as Code (IaC) setup. It either directly enables IaC as a native feature or support is via integrations. The latter is especially interesting if you want to fully leverage existing approaches such as Terraform to manage your infrastructure as code.

## Support for different types of environments

In most setups, you will have different types of environments for your applications. Your `production` environment will most likely use different infrastructure than your `development` environments. An Internal Developer Platform should allow you to configure different infrastructure depending on the type of the environment.

Many teams integrate other operational tools such as monitoring, chaos engineering, alerting or GitOps tools with IDPs at their convenience.

Learn more about integrations in this section:

{{< button relref="platform-tooling" >}}
-> Platform tooling
{{< /button >}}
