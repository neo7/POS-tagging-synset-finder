package cs481.postag;

import cs481.token.*;
import cs481.util.*;

import java.io.*;
import java.util.*;

/**
 * Determines the part of speech tags based on Viterbi.
 *
 * <pre>
 * Typical use:
 * POSTag pt = new POSTag();
 * pt.train(training);
 * pt.tag(testing);
 * </pre>
 *
 * Run from the commandline.
 *
 * @author Sterling Stuart Stein
 * @author Shlomo Argamon
 */
public class POSTag {
	/**
	 * Special start tag
	 */
	public static String StartTag = "*START*";

	/**
	 * Small probability for when not found
	 */
	public static float epsilon = -10000000f;

	/**
	 * Array of all tags
	 */
	protected String[] tags;

	/**
	 * Probability of tags given specific words Used in Good turing Smoothing.
	 */
	protected HashMap countProbability;
	/**
     * 
     */
	protected HashMap pTagWord;

	/**
	 * Probability of individual tags (i.e., P(tag)
	 */
	protected HashMap pTag;

	/**
	 * Hashmap of all known words
	 */
	protected HashMap allWords;

	/**
	 * Probability of tag given previous tag
	 */
	protected HashMap pBigramTag;

	protected HashMap tagToTagP;

	/**
	 * Counts of tags and words
	 */
	protected HashMap cWord;
	protected HashMap cTag;
	protected HashMap cTagWord;
	protected HashMap cBigramTag;

	/**
	 * Make an untrained part of speech tagger.
	 */
	public POSTag() {
		pTagWord = new HashMap();
		pTag = new HashMap();
		allWords = new HashMap();
		/**
		 * Added new HashMaps for enhancements.
		 */
		pBigramTag = new HashMap();
		cTagWord = new HashMap();
		cBigramTag = new HashMap();
		cWord = new HashMap();
		cTag = new HashMap();
		countProbability = new HashMap<>();
	}

	/**
	 * Remove all training information.
	 */
	public void clear() {
		pTag.clear();
		pTagWord.clear();
		allWords.clear();
		// clearing bigramTag
		pBigramTag.clear();
		tags = null;
	}

	/**
	 * Increment the count in a HashMap for t.
	 *
	 * @param h1
	 *            The HashMap to be modified
	 * @param t
	 *            The key of the field to increment
	 */
	protected void inc1(HashMap h1, String t) {
		if (h1.containsKey(t)) {
			int[] ip = (int[]) h1.get(t); // Used as int *
			ip[0]++;
		} else {
			int[] ip = new int[1];
			ip[0] = 1;
			h1.put(t, ip);
		}
	}

	/**
	 * Increment the count in a HashMap for [t1,t2].
	 *
	 * @param h2
	 *            The HashMap to be modified
	 * @param t1
	 *            The 1st part of the key of the field to increment
	 * @param t2
	 *            The 2nd part of the key of the field to increment
	 */
	protected void inc2(HashMap h2, String t1, String t2) {
		// Have to use Vector because arrays aren't hashable
		Vector key = new Vector(2);
		key.setSize(2);
		key.set(0, t1);
		key.set(1, t2);

		if (h2.containsKey(key)) {
			int[] ip = (int[]) h2.get(key); // Used as int *
			ip[0]++;
		} else {
			int[] ip = new int[1];
			ip[0] = 1;
			h2.put(key, ip);
		}
	}

	/**
	 * Increment the count in a HashMap for.
	 * 
	 * 
	 * @param c
	 *            has the integer count for the smoothing algo.
	 */
	private void inc3(HashMap cp, int c) {
		// TODO Auto-generated method stub
		int key = c;
		int ip;
		if (cp.containsKey(c)) {
			ip = (int) cp.get(key); // Used as int *
			/* ip++; */
			ip += 1;
			cp.put(key, ip);
		} else {
			ip = 1;
			cp.put((int) key, (int) ip);
		}
	}

	/**
	 * Train the part of speech tagger.
	 *
	 * @param training
	 *            A vector of paragraphs which have tokens with the attribute
	 *            &quot;pos&quot;.
	 */
	public void train(Vector training) {
		int cTokens = 0;

		boolean[] bTrue = new boolean[1];
		bTrue[0] = true;

		clear();

		// Count word and tag and tag-tag occurrences
		for (Iterator i = training.iterator(); i.hasNext();) {
			Vector para = (Vector) i.next();

			for (Iterator j = para.iterator(); j.hasNext();) {
				Vector sent = (Vector) j.next();// sentence vector
				String curtag = StartTag;// current tag
				String prevtag = StartTag;// previous tag
				inc1(cTag, curtag);// hashmap with current tag and its count.

				for (Iterator k = sent.iterator(); k.hasNext();) {
					Token tok = (Token) k.next();

					curtag = (String) tok.getAttrib("pos");
					inc1(cTag, curtag);

					String name = tok.getName().toLowerCase();
					inc1(cWord, name);
					allWords.put(name, bTrue);

					inc2(cTagWord, curtag, name);
					inc2(cBigramTag, prevtag, curtag);
					cTokens++;
					prevtag = curtag;
				}
			}
		}

		// Find probabilities from counts
		for (Iterator i = cTag.keySet().iterator(); i.hasNext();) {
			String key = (String) i.next();
			int[] count = (int[]) cTag.get(key);
			pTag.put(key,
					new Float(Math.log(((float) count[0]) / (float) cTokens)));
		}
		// find probability from the tag with respect to a word
		for (Iterator i = cTagWord.keySet().iterator(); i.hasNext();) {
			Vector key = (Vector) i.next();
			int[] count = (int[]) cTagWord.get(key);
			int[] total = (int[]) cWord.get(key.get(1));
			pTagWord.put(
					key,
					new Float(Math.log(((float) count[0]) / ((float) total[0]))));
		}
		// for loop to count tag given tag
		for (Iterator i = cBigramTag.keySet().iterator(); i.hasNext();) {
			Vector key = (Vector) i.next();
			int[] count = (int[]) cBigramTag.get(key);
			int[] total = (int[]) cTag.get(key.get(0));
			pBigramTag.put(
					key,
					new Float((Math
							.log(((float) count[0]) / ((float) total[0])))));
		}
		// Make list of all possible tags
		tags = (String[]) cTag.keySet().toArray(new String[0]);

		// Added as a part of Good-Turing smoothing to count the frequency of
		// words
		for (Iterator i = cTagWord.keySet().iterator(); i.hasNext();) {
			Vector key = (Vector) i.next();
			int[] count = (int[]) cTagWord.get(key);
			int c = count[0];
			inc3(countProbability, c);
		}
		// Loading property configuration
		Properties properties = loadPropertiesFile();
		String good_turing_flag = properties.getProperty("good_turing_flag");
		Boolean good_turing_flag_bool = new Boolean(good_turing_flag);

		// for finding the probability of Tag Given a word.
		if (good_turing_flag_bool) {// use good turing mechanism only if
									// configuration.
			applyGoodTuringSmoothing();
		}
	}

	private void applyGoodTuringSmoothing() {
		for (Iterator i = cTagWord.keySet().iterator(); i.hasNext();) {
			Vector key = (Vector) i.next();
			int[] count = (int[]) cTagWord.get(key);// array for Tag given Word
													// count
			int[] total = (int[]) cWord.get(key.get(1));// array for Word Count.
			int c = count[0];// getting count at 0th index.
			int rplus1count = 0; // setting turing count to 0
			int rcount;

			rcount = (int) countProbability.get(c);
			if (countProbability.containsKey(c + 1)) {
				rplus1count = (int) countProbability.get(c + 1); // increasing
																	// count
			} else {
				rplus1count = 1; // static count to one
			}

			float rstar = (float) ((c + 1) * rplus1count) / rcount;
			pTagWord.put(
					key,
					new Float(Math.log(rstar * ((float) count[0])
							/ ((float) total[0])))); // probability finding
														// step.
		}
	}

	/**
	 * This method is used for loading configuration file which is
	 * configuration.properties file. Located outside the folder structure.
	 * 
	 * @return
	 */
	private Properties loadPropertiesFile() {
		Properties properties = new Properties();
		try {
			properties.load(new FileInputStream(new File(
					"configuration.properties")));
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Error in reading file");
		}
		return properties;
	}

	/**
	 * Print out a HashMap<Vector,int[1]>.
	 *
	 * @param h
	 *            The HashMap to be printed.
	 */
	protected void debugPrintHashInt(HashMap h) {
		for (Iterator i = h.keySet().iterator(); i.hasNext();) {
			Vector key = (Vector) i.next();
			int[] ip = (int[]) h.get(key);

			for (int j = 0; j < key.size(); j++) {
				System.out.print(", " + key.get(j));
			}

			System.out.println(": " + ip[0]);
		}
	}

	/**
	 * Print out a HashMap<Vector,Float>.
	 *
	 * @param h
	 *            The HashMap to be printed.
	 */
	protected void debugPrintHashFloat(HashMap h) {
		for (Iterator i = h.keySet().iterator(); i.hasNext();) {
			Vector key = (Vector) i.next();
			float f = ((Float) h.get(key)).floatValue();

			for (int j = 0; j < key.size(); j++) {
				System.out.print(", " + key.get(j));
			}

			System.out.println(": " + f);
		}
	}

	protected void debugPrintHashKeys(HashMap h) {
		for (Iterator i = h.keySet().iterator(); i.hasNext();) {
			String key = ((String) i.next());
			System.out.println(": " + key);
		}
	}

	/**
	 * Tags a sentence by setting the &quot;pos&quot; attribute in the Tokens.
	 *
	 * @param sent
	 *            The sentence to be tagged.
	 */
	public void tagSentence(@SuppressWarnings("rawtypes") Vector sent) {
		int len = sent.size();
		if (len == 0) {
			return;
		}

		int numtags = tags.length;

		Vector twkey = new Vector(2);
		twkey.setSize(2);

		// Probability of best path to word with tag
		float[][] pathprob = new float[len + 1][numtags];

		// Edge to best path to word with tag
		int[][] backedge = new int[len + 1][numtags];

		// For words in sentence
		for (int i = 0; i < pathprob.length - 1; i++) {
			String word = ((Token) sent.get(i)).getName().toLowerCase();
			twkey.set(1, word);

			// Loop over tags for this word
			String pretag = StartTag;
			for (int j = 0; j < numtags; j++) {
				String thistag = tags[j];
				Float tagProb1 = (Float) pTag.get(thistag);
				float tagProb = (tagProb1 == null) ? epsilon : tagProb1
						.floatValue();
				twkey.set(0, thistag);

				boolean[] knownWord = (boolean[]) allWords.get(word);
				float twp = tagWordProbability(twkey, tagProb, knownWord);

				// In a unigram model, only the current probability matters
				pathprob[i][j] = twp;

				// Now create the back link to the max prob tag at the previous
				// stage
				// If we are at the second word or further
				if (i > 0) {
					int back = 0;
					float max = -100000000f;

					// Loop over previous tags
					for (int k = 0; k < numtags; k++) {
						String prevtag = tags[k];

						// Probability for path->prevtag k + thistag j->word i
						float test = pathprob[i - 1][k];

						String prevword = ((Token) sent.get(i - 1)).getName()
								.toLowerCase();

						if (test > max) {
							max = test;
							back = k;
						}
					}
					backedge[i][j] = back;// assigning bacedge to back.
				}
			}
		}

		// Trace back finding most probable path
		{
			float max = -100000000f;
			int prevtag = 0;

			// Find final tag
			for (int i = 0; i < numtags; i++) {
				float test = pathprob[len - 1][i];
				if (max < test) {
					max = test;
					prevtag = i;
				}
			}

			// Follow back edges to start tag and set tags on words
			for (int i = len - 1; i >= 0; i--) {
				Token tok = (Token) sent.get(i);
				tok.putAttrib("pos", tags[prevtag]);
				prevtag = backedge[i][prevtag];
			}
		}
	}

	/**
	 * Unigram model changed for the Bigram tagging.
	 * 
	 * @param tests
	 */
	public void bigramModel(@SuppressWarnings("rawtypes") Vector tests) {
		int len = tests.size();
		if (len == 0) {
			return;
		}
		int numtags = tags.length;

		float[][] pathprob = new float[len + 1][numtags];

		// Edge to best path to word with tag
		int[][] backedge = new int[len + 1][numtags];
		String pretag = StartTag;

		// For words in sentence
		Vector twkey = new Vector(2);
		for (int i = 0; i < pathprob.length - 1; i++) {

			String word = ((Token) tests.get(i)).getName().toLowerCase();
			twkey.setSize(2);
			twkey.set(1, word);
			// Loop over tags for this word
			Vector bigramTagKey = new Vector(2);
			bigramTagKey.setSize(2);

			for (int j = 0; j < numtags; j++) {
				HashMap tagToTagP = new HashMap();
				String thistag = tags[j];
				bigramTagKey.set(1, thistag);
				twkey.set(0, thistag);
				bigramTagKey.set(1, thistag);
				// counting probabilities
				if (pretag.equals("*START*")) {
					bigramTagKey.set(0, pretag);
					Float bigramTagProb1 = (Float) pBigramTag.get(bigramTagKey);
					float bigramTagProb = (bigramTagProb1 == null) ? epsilon
							: bigramTagProb1.floatValue();
					boolean[] knownWord = (boolean[]) allWords.get(word);
					float twp = tagWordProbability(twkey, bigramTagProb,
							knownWord);
					pathprob[i][j] = twp + bigramTagProb;
				} else {
					for (int n = 0; n < numtags; n++) {
						pretag = tags[n];
						bigramTagKey.set(0, pretag);
						int[] cpretag = (int[]) cTag.get(pretag);
						Float bigramTagProb1 = (Float) pBigramTag
								.get(bigramTagKey);
						float bigramTagProb = implementOneSmoothing(
								bigramTagProb1, cpretag);
						;
						boolean[] knownWord = (boolean[]) allWords.get(word);
						Float twp1 = (Float) pTagWord.get(twkey);
						float twp = (((knownWord == null) || (knownWord[0] != true)) ? epsilon
								: ((twp1 == null) ? epsilon : twp1.floatValue()));

						pathprob[i][j] = twp + bigramTagProb
								+ pathprob[i - 1][n];

						tagToTagP.put(pretag, pathprob[i][j]);
					}
				}

				// Now create the back link to the max prob tag at the previous
				// stage
				// If we are at the second word or further
				if (i > 0) {
					int back = 0;
					float max = -100000000f;

					// Loop over previous tags
					for (int k = 0; k < numtags; k++) {
						// String prevtag = tags[k];

						// Probability for path->prevtag k + thistag j->word i
						// System.out.println(tagToTagP.get(tags[k]));
						float test = (float) tagToTagP.get(tags[k]);

						// String prevword =
						// ((Token)tests.get(i-1)).getName().toLowerCase();
						if (test > max) {
							max = test;
							back = k;
						}
					}
					pathprob[i][j] = max;
					backedge[i][j] = back;

				}
				tagToTagP.clear();
			}
			pretag = "";
		}

		// Trace back finding most probable path
		{
			float max = -100000000f;
			int prevtag = 0;
			/*
			 * Thi s is a sample comment
			 */
			// Find final tag
			for (int i = 0; i < numtags; i++) {
				float test = pathprob[len - 1][i];
				if (max < test) {
					max = test;
					prevtag = i;
				}
			}

			// Follow back edges to start tag and set tags on words

			for (int i = len - 1; i >= 0; i--) {
				Token tok = (Token) tests.get(i);
				tok.putAttrib("pos", tags[prevtag]);
				prevtag = backedge[i][prevtag];

			}
		}

	}

	/**
	 * 
	 * @param twkey
	 * @param bigramTagProb
	 * @param knownWord
	 * @return
	 */
	private float tagWordProbability(Vector twkey, float bigramTagProb,
			boolean[] knownWord) {
		Float twp1 = (Float) pTagWord.get(twkey);
		float twp = (((knownWord == null) || (knownWord[0] != true)) ? bigramTagProb
				: ((twp1 == null) ? epsilon : twp1.floatValue()));
		return twp;
	}

	/**
	 * 
	 * @param bigramTagProb1
	 * @param cpretag
	 * @return
	 */
	private float implementOneSmoothing(Float bigramTagProb1, int[] cpretag) {
		float bigramTagProb;
		if (bigramTagProb1 == null)
			bigramTagProb = epsilon;// giving a very small probability
		else if (bigramTagProb1 == 0)
			bigramTagProb = new Float(
					Math.log((1 / ((float) cpretag[0] + (float) cTag.size()))));// creting
																				// new
																				// probability
		else {
			bigramTagProb = bigramTagProb1.floatValue();// else assigning the
														// old probability.
		}
		return bigramTagProb;
	}

	/**
	 * This method is used for calling the part of tagging method which is
	 * called.
	 * 
	 * @param testing
	 */
	public void tag(Vector testing) {
		for (Iterator i = testing.iterator(); i.hasNext();) {
			Vector para = (Vector) i.next();

			for (Iterator j = para.iterator(); j.hasNext();) {
				Vector sent = (Vector) j.next();
				bigramModel(sent);
			}
		}
	}

	/**
	 * Train on the 1st XML file, tag the 2nd XML file, write the results in the
	 * 3rd XML file.
	 *
	 * @param argv
	 *            An array of 3 XML file names.
	 */
	public static void main(String[] argv) throws Exception {
		if (argv.length != 3) {
			System.err.println("Wrong number of arguments.");
			System.err
					.println("Format:  java cs481.postag.POSTag <train XML> <test XML> <output XML>");
			System.err
					.println("Example: java cs481.postag.POSTag train.xml untagged.xml nowtagged.xml");
			System.exit(1);
		}

		Vector training = Token.readXML(new BufferedInputStream(
				new FileInputStream(argv[0])));
		System.out.println("Read training file.");

		POSTag pt = new POSTag();
		pt.train(training);
		System.out.println("Trained.");
		training = null; // Done with it, so let garbage collector reclaim

		Vector testing = Token.readXML(new BufferedInputStream(
				new FileInputStream(argv[1])));
		System.out.println("Read testing file.");
		pt.tag(testing);
		System.out.println("Tagged.");
		Token.writeXML(testing, new BufferedOutputStream(new FileOutputStream(
				argv[2])));
	}
}
