package org.axway.grapes.core.config;

import com.fasterxml.jackson.annotation.JsonProperty;

import javax.validation.Valid;

/**
 * Community configuration
 *
 * <p>Optional configuration that deals with the grapes user community. The aim is to make configurable the tools around the use of Grapes (issue tracker, documentation ...)</p>
 *
 * @author jdcoffre
 */
public class CommunityConfig{


	@Valid
    @JsonProperty
    private String issueTracker;
	
	@Valid
    @JsonProperty
    private String onlineHelp;

    public String getIssueTracker() {
        return issueTracker;
    }

    public void setIssueTracker(final String issueTracker) {
        this.issueTracker = issueTracker;
    }

    public String getOnlineHelp() {
        return onlineHelp;
    }

    public void setOnlineHelp(final String onlineHelp) {
        this.onlineHelp = onlineHelp;
    }
}
