from jpype import *

print("Begin test..")
try:
    startJVM("C:\\Program Files\\Java\\jdk1.7.0_01\\jre\\bin\\server\\jvm.dll", "-ea -Djava.class.path=C:\\Users\\Jaerod\\Documents\\GitHub\\CS361-Reading-App\\speechanalyzer")
    testPkg = JPackage('edu').cmu.sphinx.demo.speechanalyzer
    SpeechAnalyzer = testPkg.SpeechAnalyzer
    SpeechAnalyzer.main()
    shutdownJVM()
except JVMError:
	print ("JVM failure.")

print("Test complete!")
 
