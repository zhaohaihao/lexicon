package com.bigsea.scel.transform.tool;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.apache.log4j.Logger;

/**
 * 搜狗SCEL文件转换工具 Created by zhh on 2017/11/17.
 */
public class ScelTools {

	private static Logger logger = Logger.getLogger(ScelTools.class);
			 
	private static Map<Integer, String> dict = new HashMap<Integer, String>();

	private static Map<String, LinkedList<String>> wordList = new HashMap<String, LinkedList<String>>();
	
	// 当前路径
	public static String ROOT_PATH = System.getProperty("user.dir");
	
	// 当前路径上一路径
	public static String ROOT_PATH_PREV = ROOT_PATH.substring(0, ROOT_PATH.lastIndexOf("\\"));
	
	// 原始文件夹路径
	public static String ORIGINAL = ROOT_PATH_PREV + "\\sougou";
	
	// 目标文件夹路径
	public static String TARGET = ROOT_PATH_PREV + "\\sougou-txt";
	
	/**
	 * 获取scel文件路径 转成 txt
	 * @throws FileNotFoundException 
	 */
	public static void scel2txt(String filePath) {
		try {
//			System.out.println(filePath);
			readSeclFile(filePath);
//			printWordListWithPinyin();
			String content = wordList2String();
			String fileFolder = getFileFolder(filePath);
			String fileName = getFileName(filePath);
			String saveFilePath = TARGET + fileFolder;
			File saveFile = new File(saveFilePath);
			if (!saveFile.exists()) {
				saveFile.mkdirs();
			}
			saveContent2Txt(saveFilePath + "/" + fileName + ".txt" , content);
			// 清除缓存内容
			dict.clear();
			wordList.clear();
			System.out.println(">>> 文件: " + filePath + " 转写成功!");
			System.out.println(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
			System.out.println();
		} catch (Exception e) {
			e.printStackTrace();
			logger.error(">>> 文件: " + filePath + " 出现异常, 未转写成功!");
		}
	}
	
	/**
	 * 将内容保存到txt文件中
	 * @param saveFilePath 保存文件路径
	 * @param content 保持内容
	 */
	public static void saveContent2Txt(String saveFilePath, String content) {
		FileWriter fwriter = null;
		try {
			fwriter = new FileWriter(saveFilePath);
			fwriter.write(content);
		} catch (IOException ex) {
			ex.printStackTrace();
		} finally {
			try {
				fwriter.flush();
				fwriter.close();
			} catch (IOException ex) {
				ex.printStackTrace();
			}
		}
	}
	
	/**
	 * 获得 指定文件或者指定文件夹下所有文件的路径
	 * @param filePath 文件或者文件夹路径
	 * @param pathList 文件的路径列表
	 */
	public static void getAllFilePath(String filePath, List<String> pathList) {
		if (pathList == null) {
			pathList = new ArrayList<>();
		}
		if (filePath == null || "".equals(filePath)){
			return;
		}
		File file = new File(filePath);
		if (file.isDirectory()) {
			File[] childFiles = file.listFiles();
			if (childFiles != null) {
				for (File f : childFiles) {
					if (f.isDirectory()) {
						getAllFilePath(f.getPath(), pathList);
					} else {
						/* 
						 * 关于文件路径分隔符:
						 * Windows 下是"\",  unix|linux 下是"/"
						 * 考虑到程序的可移植性
						 * 对文件路径做统一替换处理
						 * "/"或 File.separator均可
						 */
						filePath = f.getAbsolutePath().replace("\\", "/");
						pathList.add(filePath);
					}
				}
			}
		} else {
			filePath = filePath.replace("\\", "/");
			pathList.add(filePath);
		}
	}

	/**
	 * 词组列表带拼音拼成字符串
	 * @return
	 */
	private static String wordListWithPinyin2String() {
		StringBuilder sb = new StringBuilder();
		for (String w : wordList.keySet()) {
			sb.append(w + Arrays.asList(wordList.get(w).toArray()));
			sb.append(System.lineSeparator());
		}
		System.out.println(">>> 当前文件词条的数量为: " + wordList.size());
		return sb.toString();
	}

	/**
	 * 词组列表拼成字符串
	 * @return
	 */
	private static String wordList2String() {
		StringBuilder sb = new StringBuilder();
		for (String w : wordList.keySet()) {
			sb.append(w);
			sb.append(System.lineSeparator());
		}
		System.out.println(">>> 当前文件词条的数量为: " + wordList.size());
		return sb.toString();
	}
	
	/**
	 * 打印词组列表带拼音
	 */
	private static void printWordListWithPinyin() {
		for (String w : wordList.keySet()) {
			System.out.println(w + Arrays.asList(wordList.get(w).toArray()));
		}
		System.out.println(">>> 当前文件词条的数量为: " + wordList.size());
	}

	/**
	 * 打印词组列表
	 */
	private static void printWordList() {
		for (String w : wordList.keySet())
			System.out.println(w);
		System.out.println(">>> 当前文件词条的数量为: " + wordList.size());
	}
	
	/**
	 * 读取secl文件
	 * @param filePath secl文件路径
	 */
	private static void readSeclFile(String filePath) {
		File file = new File(filePath);
		System.out.println(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
		System.out.println(">>> 文件: " + filePath + "正在转写, 请稍后...");
		try {
			// 只读方式打开文件
			RandomAccessFile raf = new RandomAccessFile(file, "r");

			// 开辟byte数组
			byte[] buff = new byte[128];
			// \x40\x15\x00\x00\x44\x43\x53\x01
			raf.read(buff, 0, buff.length);

			int wordPosition = 0;
			if (buff[4] == 0x44) {
				wordPosition = 0x2628;
			} else if (buff[4] == 0x45) {
				wordPosition = 0x26C4;
			}
			raf.seek(0x124);
			// 获取词的数量
//			int wordCount = readWordCount(raf);
//			System.out.println("当前文件词条的数量为: " + wordCount);
			// logger.info("当前文件词条的数量为: " + wordCount);
			
			// 获取拼音的位置
			getPinyinPosition(raf);
			
			// 获取汉字的位置
			getWordPosition(raf, wordPosition);
			raf.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/**
	 * 获取汉字的位置
	 * @param raf 文件
	 * @param wordPosition 汉字位置
	 * @throws Exception 
	 */
	private static void getWordPosition(RandomAccessFile raf, int wordPosition) throws Exception {
		raf.seek(wordPosition);
		while (true) {
			byte[] num = new byte[4];
			raf.read(num, 0, 4);
			int samePYcount = num[0] + num[1] * 256;
			int count = num[2] + num[3] * 256;

			byte[] buff = new byte[256];
			for (int i = 0; i < count; i++)
				buff[i] = raf.readByte();

			List<String> wordPY = new LinkedList<String>();
			for (int i = 0; i < count / 2; i++) {
				int key = buff[i * 2] + buff[i * 2 + 1] * 256;
				wordPY.add(dict.get(key));
			}
			// 同音词，使用前面相同的拼音
			for (int s = 0; s < samePYcount; s++) {
				raf.read(num, 0, 2);
				int hzBytecount = num[0] + num[1] * 256;
				// System.out.println("hzBytecount:" + hzBytecount);
				raf.read(buff, 0, hzBytecount);
				String word = getString(buff, hzBytecount);
				// System.out.println(word);
				raf.readShort();
				raf.readInt();
				wordList.put(word, (LinkedList<String>) wordPY);

				for (int i = 0; i < 6; i++) {
					raf.readByte();
				}
			}
			if (raf.getFilePointer() == raf.length())
				break;
		}
	}
	
	/**
	 * 获取拼音的位置
	 * @param raf 文件
	 * @throws Exception
	 */
	private static void getPinyinPosition(RandomAccessFile raf) throws Exception {
		raf.seek(0x1544);
		while (true) {
			byte[] b = new byte[4];
			raf.read(b, 0, b.length);
			int mark = b[0] + b[1] * 256;

			byte[] buff = new byte[20];
			raf.read(buff, 0, b[2]);
			String py = getString(buff, b[2]);
			dict.put(mark, py);
			if (py.equals("zuo")) {
				break;
			}
		}
	}
	
	/**
	 * 获取字数
	 * @param raf 文件
	 * @return
	 * @throws Exception
	 */
	private static int readWordCount(RandomAccessFile raf) throws Exception {
		byte[] buff = new byte[4];
		raf.read(buff, 0, buff.length);
		return (int) buff[0] & 0xFF + (((int) buff[1] & 0xFF) << 8) + (((int) buff[2] & 0xFF) << 16)
				| (((int) buff[3] & 0xFF) << 24);
	}

	/**
	 * 获取文字字符串
	 * @param buff 缓冲区
	 * @param num 汉字位数
	 * @return
	 * @throws Exception
	 */
	private static String getString(byte[] buff, int num) throws Exception {
		String str = new String(buff, 0, num, "UTF-16LE");
		return str;
	}
	
	/**
	 * 获取文件名
	 * @param filePath 文件路径
	 * @return
	 */
	private static String getFileName(String filePath) {
		int pos = filePath.lastIndexOf("/");
		if (pos != -1) {
			String fileNameWithSuffix = filePath.substring(pos + 1);
			int suffixPos = fileNameWithSuffix.lastIndexOf(".");
			if (suffixPos != -1) {
				return fileNameWithSuffix.substring(0, suffixPos);
			}
			return filePath.substring(pos + 1);
		}
		return "";
	}
	
	/**
	 * 获取文件夹分类
	 * @param filePath 文件路径
	 * @return
	 */
	private static String getFileFolder(String filePath) {
		filePath = filePath.substring(ROOT_PATH_PREV.length());
		int fileNamePos = filePath.lastIndexOf("/");
		filePath = filePath.substring(0, fileNamePos);
		filePath = filePath.replaceAll("/sougou", "");
		return filePath;
	}
}
