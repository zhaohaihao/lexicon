package com.bigsea.scel.transform.main;

import java.util.ArrayList;
import java.util.List;

import com.bigsea.scel.transform.tool.ScelTools;

/**
 * 启动项目
 * Created by zhh on 2017/11/17.
 */
public class AppMain {
	public static void main(String[] args) throws Exception {
		System.out.println(ScelTools.ROOT_PATH);
		System.out.println(ScelTools.ROOT_PATH_PREV);
		System.out.println(ScelTools.ORIGINAL);
		System.out.println(ScelTools.TARGET);
		List<String> pathList = new ArrayList<String>();
		ScelTools.getAllFilePath(ScelTools.ORIGINAL, pathList);
		for (String string : pathList) {
			ScelTools.scel2txt(string);
		}
	}
}
