# Kotlin adoption on the Android open source community
This repository contains the implementation used for the post `Kotlin adoption on Android open source community` [published on Medium]().   

### Datasets
[creations_scrapper](creations_scrapper.py) fetchs the number of Github repositories created every month from `2016-02-15` (Kotlin release date) to `2019-01-15`, creating four distinct categories:

| Category | Scope | Main Language | Github Query |
|----------------|---------------|---------------|----------------|
| Android + Kotlin | Only Android projects  | Kotlin | `android language:kotlin`|
| Android + Java   | Only Android projects  | Java | `android language:java` |
| Not Android + Kotlin | Not Android projects  | Kotlin | `NOT android language:kotlin`|
| Not Android + Java | Not Android projects  | Java | `NOT android language:java`|

Thus, Android repositories are those which contain the `android` word in their title, description or readme file. Alike, not Android repositories are those which does not contain the `android` word in their title, description or readme. This is a very coarse way of filtering them, but it's also a pretty convenient one. Suggestions are welcome.

[migrations_scrapper](creations_scrapper.py) fetchs those active Github Android repositories which have been and have not been migrated to Kotlin. 

For getting the migrated repositories, it retrieves those Java repositories which were created before Kotlin was released and now their main language is Kotlin (I was not able to find what percentage it represents, I'd guess 50%?). The Github query used is: `android language:kotlin created:<2016-02-15 pushed:>2019-01-01`. 

In like manner, to get those which have not been (yet?) migrated, the script retrieves those Java repositories which were created before Kotlin was released and their main language is still Java. The Github query used is: `android language:java created:<2016-02-15 pushed:>2019-01-01`. 

The main limitation of this approach is that all the Java repositories which were created after Kotlin was released and migrate to Kotlin after that point are ignored. 
 
### Data analysis
This clumsy study aims to evaluate the adoption of the Kotlin programming language on the Android open source community. To do so, it addresses several points by which descriptive and comparative analyses will put into perspective the question. Both [creations_DEA](creations_DEA.ipynb) and [migrations_DEA](migrations_DEA.ipynb) address these points: 


1. Compare the ratio of Android repositories created in Kotlin vs Java in a monthly bases and check if it shows an increasing/decreasing trend.
2. Compare the previous rate with the not Android community one.
3. Evaluate if the public support from Google had any inpact in the previous rate.
4. Determine how many active Android repositories have been migrated from Java to Kotlin.
2. Check if the repositories migrated show any common attributes (popularity and size).