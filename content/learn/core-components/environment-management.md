+++
title="Environment Management"
url="/core-components/environment-management"
weight=30
+++

# Environment Management

{{< hint info >}}
TLDR; Internal Developer Platforms (IDPs) allow developers to self-serve new environments on demand. This removes a lot of bottlenecks and enables faster delivery. Each new environment is provisioned as defined by the DevOps team.
{{< /hint >}}

From a developer perspective, Environment Management is one of the most interesting components of an Internal Developer Platform. In many existing setups, setting up a new environment typically involves waiting for someone else (most likely the DevOps team) to create and configure the new environment. This is annoying for everybody involved and also costly. An Internal Developer Platform eliminates all the required manual steps and enables self-service for the developer (or other people in your team) to spin up a new environment whenever needed.

## Typical challenges without an Internal Developer Platform

There are a number of typical challenges when it comes to Environment Management. Some of them are quite obvious and some are not.

- Typically, setting up a new environment requires reaching out to another team (e.g., the DevOps or platform team). You then have to wait for the other team to provide you with the requested environment. This might take hours if everything is well organized but might also take days or even weeks if the team is working on other priorities.
- When setting up new environments is difficult, you will most likely not switch off environments when not in use. Instead you will just keep them in case you need them again. This results in resources idling (but still costing money).
- Not being able to create new environments when needed can have a significant impact on your speed of delivery. An example is when shared environments are blocked for days or even weeks because one team needs to test a hotfix that needs to go to `production` asap, or because QA is testing a new feature that is hard and time-consuming to test. While these environments are blocked, other teams are not able to test their own new services or features. Be aware that this is not an infrequent problem (as in the cases mentioned) but happens every single day on a lesser basis.

In general, infrastructure, application configurations, and the real environments are often managed in silos from both, a technical as well as an organizational point of view. The following picture illustrates this:
{{< figure link="/_assets/images/environment-management-before.png" src="/_assets/images/environment-management-before.png" caption="Infrastructure, application configurations, and environments are typically managed in silos" alt="environment-management-before.png" >}}

## Typical approach with an Internal Developer Platform

An Internal Developer Platform typically connects infrastructure (see also [Infrastructure Orchestration]({{< relref "infrastructure-orchestration" >}})), application configurations (see also [Application Configuration Management]({{< relref "application-configuration-management" >}})), and the management of environments. The following picture illustrates this.
{{< figure link="/_assets/images/environment-management-after.png" src="/_assets/images/environment-management-after.png" caption="Internal Developer Platforms tie together infrastructure, application configurations, and environments to boost the developer experience" alt="environment-management-after.png" >}}

There are a number of different elements in how Internal Developer Platforms support Environment Management:

- **Self service:** An Internal Developer Platform enables developers or teams to create new environments when needed. New environments are created within the context of an application typically by cloning an existing deployment to a new environment. The developer can then alter the newly created environment however needed (e.g., to test a new service or feature branch). All of this should happen based on infrastructure that is provided and maintained by the DevOps team. Internal Developer Platforms typically provide different ways to create new environments via a user interface (UI), a command-line interface (CLI), or an API - which is typically the best solution for fully-automated environment creation (e.g., for automated end-to-end tests). An Internal Developer Platform should also support automated teardown or pausing of environments if they are not needed to avoid unnecessary costs.
- **Environments types:** Typically, an Internal Developer Platform allows the DevOps team to define different types of environments (see also [Infrastructure Orchestration]({{< relref "infrastructure-orchestration" >}})). This ensures new environments are created with reasonable infrastructure requirements (e.g., small machines for `development` environments and a powerful setup for `production` or a `loadtest` environment).
