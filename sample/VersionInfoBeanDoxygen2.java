/*! Doxygen block
 */
package it.is.just.a.test;

import java.io.Serializable;

import javax.faces.bean.ApplicationScoped;
import javax.faces.bean.ManagedBean;

@ManagedBean(name = "versionBean")
@ApplicationScoped
public class VersionBean implements Serializable {

	private static final long serialVersionUID = 1L;

	public VersionBean() {
	}
	
	public String getVersion() {
		return null;
	}
}

