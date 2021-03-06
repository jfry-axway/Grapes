package org.axway.grapes.core.handler;

import org.apache.felix.ipojo.annotations.Requires;
import org.axway.grapes.core.options.FiltersHolder;
import org.axway.grapes.core.options.filters.CorporateFilter;
import org.axway.grapes.core.reports.DepedencyReport2;
import org.axway.grapes.core.reports.DependencyReport;
import org.axway.grapes.core.service.ArtifactService;
import org.axway.grapes.core.service.DependencyService;
import org.axway.grapes.core.service.ModuleService;
import org.axway.grapes.core.service.VersionsService;
import org.axway.grapes.core.webapi.resources.DependencyComplete;
import org.axway.grapes.model.datamodel.Artifact;
import org.axway.grapes.model.datamodel.Dependency;
import org.axway.grapes.model.datamodel.Module;
import org.axway.grapes.model.datamodel.Organization;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.wisdom.api.annotations.Service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.NoSuchElementException;

/**
 * Created by jennifer on 4/28/15.
 */
@Service
public class DependencyHandler implements DependencyService {

    private static final Logger LOG = LoggerFactory.getLogger(DependencyHandler.class);
    @Requires
    ModuleService moduleService;
    @Requires
    ArtifactService artifactService;
    @Requires
    VersionsService versionsService;
    @Requires
    DataUtils dataUtils;

    @Override
    public List<Dependency> getModuleDependencies(String moduleId, FiltersHolder filters) {

        final Module module = moduleService.getModule(moduleId);
        final Organization organization = moduleService.getOrganization(module);
        filters.setCorporateFilter(new CorporateFilter(organization));
        return getModuleDependencies(module, filters, 1, new ArrayList<String>());
    }

    private List<Dependency> getModuleDependencies(final Module module, final FiltersHolder filters, final int depth, final List<String> doneModuleIds) {
        // Checks if the module has already been done

        if (module == null || doneModuleIds.contains(module.getId())) {
//
            return Collections.<Dependency>emptyList();
        } else {
            doneModuleIds.add(module.getId());
        }
        final List<Dependency> dependencies = new ArrayList<Dependency>();
        for (Dependency dependency : dataUtils.getAllDbDependencies(module)) {

            if (filters.shouldBeInReport(dependency)) {

                dependencies.add(dependency);
                if (filters.getDepthHandler().shouldGoDeeper(depth)) {

                    final Module dependencyModule = moduleService.getRootModuleOf(dependency.getTarget());
                    //todo if rootmodual is the same as original module no need to recall this

                    dependencies.addAll(getModuleDependencies(dependencyModule, filters, depth + 1, doneModuleIds));
                }
            }
        }
        return dependencies;
    }

    @Override
    public DepedencyReport2 getDependencyReport(String moduleId, FiltersHolder filters) {

        final Module module = moduleService.getModule(moduleId);
        List<Dependency> dependencyList = getModuleDependencies(moduleId, filters);

        final Organization organization = moduleService.getOrganization(module);
        filters.setCorporateFilter(new CorporateFilter(organization));
        final DepedencyReport2 report = new DepedencyReport2();
        for(Dependency dependency: dependencyList) {
            try {
                Artifact target = artifactService.getArtifact(dependency.getTarget());
                report.addDependency(dependency,versionsService.getLastVersion(target,false),target);
            } catch (NoSuchElementException e){
            LOG.error(e.getMessage());
        }
        }
        return report;
    }
    private void addModuleToReport(final DependencyReport report, final Module module, final FiltersHolder filters, final List<String> done, final int depth) {
        if (module == null || done.contains(module.getId())) {
            return;
        }
        done.add(module.getId());
        for (Dependency dependency : dataUtils.getAllDbDependencies(module)) {
            addDependenciesToReport(report, dependency, filters, done, depth);
        }
    }


    private void addDependenciesToReport(final DependencyReport report, final Dependency dbDependency, final FiltersHolder filters, final List<String> done, final int depth) {
        final Artifact artifact = artifactService.getArtifact(dbDependency.getTarget());
        if (artifact == null) {
            return;
        }
        if (filters.shouldBeInReport(dbDependency)) {
            if (artifact.getDoNotUse()) {
                report.addShouldNotUse(artifact.getGavc());
            }
            String lastRelease = null;
            try {
                lastRelease = versionsService.getLastRelease(artifactService.getArtifactVersions(artifact));
            } catch (Exception e) {
                LOG.info("Failed to find the latest artifact release version: " + artifact.getVersion());
            }
            final DependencyComplete dependency = new DependencyComplete();
            dependency.setTarget(artifact);
            dependency.setScope(dbDependency.getScope());
            dependency.setSourceName(dataUtils.getModuleName(dbDependency.getSource()));
            dependency.setSourceVersion(dataUtils.getModuleVersion(dbDependency.getSource()));
            report.addDependency(dependency, lastRelease);
        }
        if (filters.getDepthHandler().shouldGoDeeper(depth)) {
            final Module module = moduleService.getRootModuleOf(dbDependency.getTarget());
            addModuleToReport(report, module, filters, done, depth + 1);
        }
    }
}
