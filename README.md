# <img src="misc/fables.png" alt="FABLES" width="150" height="40"> : [Evaluating faithfulness and content selection in book-length summarization](https://arxiv.org/pdf/2404.01261.pdf)
[![arXiv](https://img.shields.io/badge/arXiv-2404.01261-b31b1b.svg)](https://arxiv.org/abs/2404.01261)

This repo hosts `FABLES` (Faithfulness Annotations for Book-Length Summarization), a dataset of model-generated summaries with atomic claims annotated for faithfulness. More updates coming soon!

`Authors`: Yekyung Kim, Yapei Chang, Marzena Karpinska, Aparna Garimella, Varun Manjunatha, Kyle Lo, Tanya Goyal, Mohit Iyyer

## Introduction
While long-context large language models (LLMs) can technically summarize book-length documents (> 100K tokens), the length and complexity of the documents have so far prohibited evaluations of input-dependent aspects like faithfulness. In this paper, we conduct the first large-scale human evaluation of faithfulness and content selection on LLM-generated summaries of fictional books. Our study mitigates the issue of data contamination by focusing on summaries of books published in 2023 or 2024, and we hire annotators who have fully read each book prior to the annotation task to minimize cost and cognitive burden. In total, we collect annotations on 3,158 claims made in LLM-generated summaries of 26 books at a cost of $5.2K USD, which allows us to rank LLM summarizers based on faithfulness: CLAUDE-3-OPUS significantly outperforms all closed-source LLMs, while the open-source MIXTRAL is on par with GPT-3.5-TURBO. An analysis of the annotations reveals that most unfaithful claims relate to events and character states, and they generally require indirect reasoning over the narrative to invalidate. While LLM-based auto-raters have proven reliable for factuality and coherence in other settings, we implement several LLM raters of faithfulness and find that none correlates strongly with human annotations, especially with regard to detecting unfaithful claims. Our experiments suggest that detecting unfaithful claims is an important future direction not only for summarization evaluation but also as a testbed for long-context understanding. Finally, we move beyond faithfulness by exploring content selection errors in book-length summarization: we develop a typology of omission errors related to crucial narrative elements and also identify a systematic over-emphasis on events occurring towards the end of the book. We will release our annotations to spur further research on the evaluation of book-length summarization.

![Pipeline of work](./misc/pipeline-1.png)

## Data

`FABLES` is a dataset created from book-length summaries of narrative books published in 2023-2024. The data contains:

🪄 `Book Title` -- Title of the book used for summarization. Each title is a `dict` contaitning data related to the book.

🪄 `Model Name` -- Name of the model that summariezed the book: MIXTRAL, GPT-3.5-TURBO, GPT-4, GPT-4-TURBO, or CLAUDE-3-OPUS. A `dict` containing all summary data for that model.

🪄 `General Comment` -- (`str`) Overview of issues with the set of claims, including omissions of important information, chronology, salience (mention of unimportant events/details), factuality, and others like repetitiveness or vagueness, with each summary receiving a comment.

🪄 `Summary` -- (`str`) Entire book summarized by one of five models: Mixtral, GPT-3.5-Turbo, GPT-4, GPT-4-Turbo, and Claude-3-Opus, using the hierarchical merging method described in [Chang et al.](https://arxiv.org/pdf/2310.00785.pdf).

🪄 `Claims` -- (`dict`)  Numbered dictionary of decontextualized claims from each summary extracted using GPT-4.

🪄 `Label` -- (`str`) Faithfulness label assigned by native English-speaking annotators based on their reading. Labels are **"Yes"** (accurate reflection), **"No"** (misrepresentation), **"PartialSupport"** (partially corroborated), or **"Inapplicable"** (indeterminable), applied to each claim.

🪄 `Reason` -- (`list`) List of reasons provided by annotator' as a justification for each faithfulness label (provided for some claims).

🪄 `Evidence` -- (`list`) List of evidence, source text quotations, provided by annotators to support their labels (available for most claims).

FALBES data is stored in a JSON file, formatted as follows (where 'book title' and 'model name' are placeholders for their actual values):

```markdown
* `book title`: (str) 
  * `model name`: (str) 
    *  `summary`: (str) 
    *  `general_comment`: (str)
    *  `claims`: (dict)
       * `claim`: (str)
       * `label`: (str)
       * `evidence`: (list of str)
       * `reason`: (list of str)
```
Note: In the `claims` dictionary, each claim is indexed numerically as a key, with each key pointing to a dictionary containing the fields `claim`, `label`, `evidence`, and `reason`.

Example entry:

```json
{
  "Wildfire": {
    "CLAUDE-3-OPUS": {
      "general_comment": "This summary is largely chronological (though Aurora's decision to not attend her father's wedding comes after Russ' father's visit) and hits the main thematic elements of the text, though it disproportionately addresses the epilogue over other portions of the text. The claims are factual, however.",
      "summary": "Wildfire, the first book in the Icebreaker series, follows the love story of Aurora Roberts and Russ Callaghan, two college students who meet while working as counselors at Honey Acres, a sleepaway summer camp in California. Aurora, the daughter of a famous Formula 1 team owner, struggles with her distant father's lack of attention and affection, often acting out to gain his notice but facing continual disappointment. Russ, a reserved hockey player at UC Maple Hills, deals with the shame and embarrassment of his father's gambling addiction, which has strained their family relationships.(...)",
      "claims": {
        "0": {
          "claim": "The book 'Wildfire' is the first in the Icebreaker series.",
          "label": "No",
          "evidence": ["n/a"],
          "reason": ["Not quoted in the book, but this is the second in the series, after 'Icebreaker'."]
        }
      }
    }
  }
}

```
  

### Corpus Statistics

|                    | **Books (Documents)** | **Books (Summaries)** | **Books (Claims)** | **Annotations (Reasons)** | **Annotations (Evidence)** | **Annotations (Comments)** |
|--------------------|-----------------------|-----------------------|--------------------|---------------------------|----------------------------|----------------------------|
|                    |       (n=26)          |       (n=130)         |      (n=3,158)     |        (n=1,513)          |          (n=3,051)         |          (n=130)           |
| **Mean**           | 121,467               | 594.3                 | 19.8               | 37.6                      | 194.7                      | 155                        |
| **St. dev.**       | 35,836                | 119.5                 | 6.4                | 33.4                      | 218.5                      | 148.4                      |
| **Max**            | 243,965               | 798                   | 58                 | 281                       | 2,435                      | 823                        |
| **Min**            | 49,762                | 172                   | 6                  | 2                         | 5                          | 6                          |


Number of tokens across books and annotations (`v1`); based on [`tiktoken`](https://github.com/openai/tiktoken) tokenizer.

Please note that the full source texts, being copyrighted, are not included in our release. However, we provide a [list](https://github.com/mungg/FABLES/blob/main/booklist.md) of the books for purchase, facilitating further investigation into summary accuracy and claim verification.

### Dataset Example

Summary:
>Romantic Comedy follows Sally, a talented Emmy-winning comedy writer for the hit TV show, "The Night Owls" (TNO), and her tumultuous journey through work, friendships, and romantic interests. The narrative delves into the chaotic, thrilling backstage antics of TNO, showcasing the stress, joy, and exhaustion that come with producing and performing a live comedy show. It outlines the complex professional dynamics within the industry, featuring colleagues such as Danny, who is engaged to the celebrity, Annabel Lily, as well as Viv and Henrietta, both TNO cast members. Sally also has to deal with an unresolved romantic past with Elliot, who is the head of TNO's writing department.  Her life takes a turn when she meets the show's guest host, Noah Brewster, a popular musician. Their bond deepens as they share intimate conversations revolving around their backgrounds, notably Sally's education at Duke University and Noah's decision to skip college for music. As their friendship blossoms amidst the backdrop of a global pandemic, Sally finds herself increasingly drawn to Noah, leading to an intricate email exchange about personal struggles, regrets, and ongoing lifestyle changes.  Balancing her professional responsibilities with her evolving personal life, Sally embarks on a solo drive from Kansas City to Los Angeles to visit Noah. Amidst their blooming romance, they have intimate conversations about past relationships, fears, and anxieties over their impending meeting. Noah openly discloses a past relationship with a woman named Louisiana, a revelation that deepens their understanding of each other.  Their relationship grows amid various hurdles, including a public break-up between Danny and Annabel which disrupts a live broadcast, Sally's former partner Jerry falling gravely ill, and escalating public scrutiny over leaked private photos of Sally and Noah together. Despite these challenges, Sally and Noah manage to navigate their intricately entangled lives, always gravitating back to one another.  Noah, cherishing his love for Sally more than his celebrity life, is unwavering in his affection towards her, even when her role in his public life becomes controversial due to increased paparazzi attention. Undeterred by the mounting challenges, intimate vulnerabilities are shared, fostering a deep intimacy between the two. At one point, Noah suggests that Sally stay in LA, which though jolts Sally's anxiety, signifies their strengthening bond.  Faced with the severity of Jerry's illness, speculated to be Covid-19, Sally and Noah return to Kansas to take care of him. Their shared experience propels them to reassess their relationship, eventually leading to Sally's decision to resign from TNO. Their bond culminates in a private wedding ceremony and their decision to settle in Kansas City. While Noah continues to create music, Sally embarks on a successful career as a scriptwriter in LA.  In this comedic roller coaster journey, the narrative skillfully depicts the convergence of their professional and personal lives, despite the complexities presented by the public spotlight, unresolved romances, and the pandemonium of the television industry. This not only strengthens their relationship but also allows Sally to find beauty in their shared growth, intricacies, and the absurdities of life. The story wraps up with Sally and Noah cherishing their bond, navigating their unique circumstances, and embracing their evolving roles in each other's lives amongst the backdrop of the chaotic TV industry.

General Comment:
>This is a well structured summary. The story progression is communicated very effectively and it is easily to get the overall plot of the book from it. In one claim Jerry is erroneously marked as Sally's partner, but overall the claims are accurate.

Labled Claims:
| # | Claim                                                                                                               | Label        |
|---|-----------------------------------------------------------------------------------------------------------------------------|-----------------|
| 0 | Romantic Comedy is a story that follows Sally, an Emmy-winning comedy writer for the hit TV show, "The Night Owls" (TNO).   | Yes             |
| 1 | The narrative details the backstage antics of producing and performing a live comedy show, "The Night Owls".               | Yes             |
| 2 | The story features several characters in the TV industry including Danny who is engaged to celebrity Annabel Lily, and Viv and Henrietta who are both TNO cast members. | Yes             |
| 3 | Elliot, who is the head of TNO's writing department, has an unresolved romantic past with Sally.                           | PartialSupport  |
| 4 | Sally, the main character, meets Noah Brewster, a popular musician, who is a guest host on the show.                       | Yes             |
| 5 | Sally and Noah Brewster bond over intimate conversations about their backgrounds, including Sally's education at Duke University and Noah's decision to skip college for music. | Yes             |
| 6 | Amidst a global pandemic, Sally finds herself increasingly attracted to Noah.                                               | Yes             |
| 7 | Sally and Noah engage in an intricate email exchange discussing personal struggles, regrets, and ongoing lifestyle changes. | Yes             |
| 8 | Sally embarks on a solo drive from Kansas City to Los Angeles to visit Noah Brewster.                                       | Yes             |
| 9 | During their blossoming relationship, Sally and Noah have intimate conversations about past relationships, fears, and anxieties. | Yes             |
| 10| Noah discloses a past relationship with a woman named Louisiana, deepening their mutual understanding.                      | Yes             |
| 11| Their relationship faces hurdles including a public break-up between Danny and Annabel, the serious illness of Sally's former partner Jerry, and leaked private photos of Sally and Noah. | PartialSupport  |



## Disclaimer

The narratives included in this dataset explore a range of themes, some of which may be sensitive, including mental health struggles such as depression, murder, and suicide.


## Citation Information
If you use this dataset, please cite it as follows:
```
@misc{fables-2024-kim-et-al,
author = {Kim, Yekyung and Chang, Yapei and Karpinska, Marzena and Garimella, Aparna and Manjunatha, Varun and Lo, Kyle and Goyal, Tanya and Iyyer, Mohit},
month = {4},
title = {FABLES: Evaluating faithfulness and content selection in book-length summarization},
url = {https://arxiv.org/abs/2404.01261},
year = {2024}
}
```
