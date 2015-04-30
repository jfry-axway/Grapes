package org.axway.grapes.jongo.model;

import org.axway.grapes.model.datamodel.Scope;
import org.axway.grapes.jongo.datamodel.DbDependency;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

public class DbDependencyTest {

    @Test
    public void checkThatTwoDependenciesAreEquals(){
        final DbDependency dependency1 = new DbDependency("source", "target", Scope.RUNTIME );
        assertEquals(dependency1, dependency1);

        DbDependency dependency2 = new DbDependency();
        assertNotEquals(dependency1, dependency2);

//        dependency2 = new DbDependency("source", null, null);
//        assertNotEquals(dependency1, dependency2);

        dependency2 = new DbDependency("source", "target", null);
        assertNotEquals(dependency1, dependency2);

        dependency2 = new DbDependency("source", "target", Scope.COMPILE);
        assertNotEquals(dependency1, dependency2);

        dependency2 = new DbDependency("source", "target", Scope.RUNTIME);
        assertEquals(dependency1, dependency2);
    }
}
