package com.jeremyc;

import java.io.File;
import java.util.List;
import java.util.ArrayList;

import net.masterthought.cucumber.Configuration;
import net.masterthought.cucumber.ReportBuilder;
import net.masterthought.cucumber.presentation.PresentationMode;


/**
 * See:
 * https://github.com/damianszczepanik/cucumber-reporting
*/

public class GenerateExtraReports {

	private void addJsonFile(String filePath, List<String> jsonFiles) {
		File f = new File(filePath)
		if (f.exists()) {
			jsonFiles.add(filePath);
		} else {
			System.err.println("WARNING: GenerateExtraReports: Ignoring missing file: " + filePath);
		}
	}

	public static void main(String args[]) {

		File reportOutputDirectory = new File("reports/html");

		// Point to our input .json files.
		List<String> jsonFiles = new ArrayList<String>();
		addJsonFile("reports/TESTS-cucumber-acceptance.json", jsonFiles);
		if (jsonFiles.size() == 0) {
			SYstem.err.println("WARNING: GenerteExtraReports: No json files to convert to html!");
			return
		}

		String buildNumber = "1";
		String projectName = "cucumberProject";
		Configuration configuration = new Configuration(reportOutputDirectory, projectName);
		configuration.setBuildNumber(buildNumber);

		// JeremyC. Not sure what this is.
		// optional configuration - check javadoc for details
		configuration.addPresentationModes(PresentationMode.RUN_WITH_JENKINS);

		// JeremyC. Not sure what this is.
		// addidtional metadata presented on main page
		configuration.addClassifications("Platform", "Windows");
		configuration.addClassifications("Browser", "Firefox");
		configuration.addClassifications("Branch", "release/1.0");

		// JeremyC. Not sure what this is.
		// optionally add metadata presented on main page via properties file
		//List<String> classificationFiles = new ArrayList<String>();
		//classificationFiles.add("properties-1.properties");
		//classificationFiles.add("properties-2.properties");
		//configuration.addClassificationFiles(classificationFiles);

		ReportBuilder reportBuilder = new ReportBuilder(jsonFiles, configuration);
		reportBuilder.generateReports();
	}

}
