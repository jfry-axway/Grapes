package org.axway.grapes.model.utils;


import org.junit.Test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URL;

import static junit.framework.TestCase.*;

public class FileUtilsTest {

    @Test
    public void checkSerialization() throws IOException {
        final File testdir = new File(System.getProperty("user.dir") + "/target");
        final String content = "content";
        final String fileName = "test.txt";

        final File testFile = new File(testdir, fileName);
        assertFalse(testFile.exists());

        FileUtils.serialize(testdir, content, fileName);
        assertTrue(testFile.exists());

        FileReader reader = null;
        BufferedReader buff = null;
        String realContent = null;

        try{
            reader = new FileReader(testFile);
            buff = new BufferedReader(reader);

            realContent = buff.readLine();

        }
        catch (Exception e){

        }
        finally {
            if(buff != null){
                try {
                    buff.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if(reader != null){
                try {
                    reader.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        assertNotNull(realContent);
        assertEquals(content, realContent);

        if(testFile.exists()){
            testFile.delete();
        }

    }

    @Test
    public void checkReadMethod() throws IOException {
        final URL testFile = Thread.currentThread().getContextClassLoader().getResource("org/axway/grapes/model/utils/file.txt");

        assertNotNull(testFile);
        assertEquals("Can you read this?", FileUtils.read(new File(testFile.getPath())));
    }


}
