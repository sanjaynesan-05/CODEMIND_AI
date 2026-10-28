"""Standard-input versions of the original fundamentals for C/Python/Java."""


FUNDAMENTALS = {
    "running-sum": {
        "category": "Loops and Accumulation", "entry": "main.py",
        "description": "Read n followed by n integers. Print the running total after each value.",
        "tests": [{"input": "4\n1 2 3 4\n", "expected_output": "1 3 6 10"}, {"input": "3\n5 -2 4\n", "expected_output": "5 3 7"}, {"input": "1\n9\n", "expected_output": "9"}],
        "examples": [{"input": "4\n1 2 3 4", "output": "1 3 6 10"}], "constraints": ["1 <= n <= 100,000"],
        "starters": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];values=d[1:1+n]\n# Add each value to a running total.\nprint(*[])\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();/* Print the running total after each value. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;/* Print each running total. */}\n",
        },
        "solutions": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));total=0;out=[]\nfor v in d[1:1+d[0]]:total+=v;out.append(total)\nprint(*out)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long sum=0;for(int i=0;i<n;i++){sum+=s.nextLong();System.out.print((i>0?\" \":\"\")+sum);}}}",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long sum=0,v;for(int i=0;i<n;i++){scanf(\"%lld\",&v);sum+=v;printf(\"%s%lld\",i?\" \":\"\",sum);}}",
        },
    },
    "sum-list": {
        "category": "Loops and Accumulation", "entry": "main.py",
        "description": "Read n followed by n integers. Print their sum (0 for an empty list). Practice a running total.",
        "tests": [{"input": "3\n1 2 3\n", "expected_output": "6"}, {"input": "2\n-2 5\n", "expected_output": "3"}, {"input": "0\n", "expected_output": "0"}],
        "examples": [{"input": "3\n1 2 3", "output": "6"}], "constraints": ["0 <= n <= 100,000"],
        "starters": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];nums=d[1:1+n]\n# Add each number to a running total.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();/* Add each input number to a running total. */System.out.println(0);}}\n",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;/* Read and add n numbers. */puts(\"0\");}\n",
        },
        "solutions": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));print(sum(d[1:1+d[0]]))",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long total=0;for(int i=0;i<n;i++)total+=s.nextLong();System.out.println(total);}}",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long sum=0,v;for(int i=0;i<n;i++){scanf(\"%lld\",&v);sum+=v;}printf(\"%lld\\n\",sum);}",
        },
    },
    "count-vowels": {
        "category": "Strings", "entry": "main.py",
        "description": "Read one line and print the number of English vowels (a, e, i, o, u), ignoring letter case.",
        "tests": [{"input": "Codemind\n", "expected_output": "3"}, {"input": "AEIOU\n", "expected_output": "5"}, {"input": "rhythm\n", "expected_output": "0"}],
        "examples": [{"input": "CodeMind", "output": "3"}], "constraints": ["Line length is at most 100,000 ASCII characters."],
        "starters": {
            "python": "import sys\ntext=sys.stdin.readline().rstrip('\\n')\n# Count vowels without treating uppercase letters differently.\nprint(0)\n",
            "java": "import java.io.*;\npublic class Main {public static void main(String[]x)throws Exception{String text=new BufferedReader(new InputStreamReader(System.in)).readLine();/* Count vowels without case sensitivity. */System.out.println(0);}}\n",
            "c": "#include <stdio.h>\nint main(void){char text[100005];fgets(text,sizeof(text),stdin);/* Count vowels without case sensitivity. */puts(\"0\");}\n",
        },
        "solutions": {
            "python": "import sys\ns=sys.stdin.readline().lower();print(sum(ch in 'aeiou' for ch in s))",
            "java": "import java.io.*;\npublic class Main {public static void main(String[]x)throws Exception{String s=new BufferedReader(new InputStreamReader(System.in)).readLine();int n=0;if(s!=null)for(char c:s.toLowerCase().toCharArray())if(\"aeiou\".indexOf(c)>=0)n++;System.out.println(n);}}",
            "c": "#include <stdio.h>\n#include <ctype.h>\nint main(void){char s[100005];if(!fgets(s,sizeof(s),stdin))return 0;int n=0;for(int i=0;s[i];i++){int c=tolower((unsigned char)s[i]);if(c=='a'||c=='e'||c=='i'||c=='o'||c=='u')n++;}printf(\"%d\\n\",n);}",
        },
    },
    "is-even": {
        "category": "Math & Logic", "entry": "main.py",
        "description": "Read an integer and print true if it is even, otherwise false.",
        "tests": [{"input": "4\n", "expected_output": "true"}, {"input": "7\n", "expected_output": "false"}, {"input": "0\n", "expected_output": "true"}, {"input": "-2\n", "expected_output": "true"}],
        "examples": [{"input": "7", "output": "false"}], "constraints": ["Input fits in a signed 64-bit integer."],
        "starters": {
            "python": "import sys\nnumber=int(sys.stdin.readline())\n# Use the remainder after division by two.\nprint(False)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);long n=s.nextLong();/* Check the remainder after division by two. */System.out.println(false);}}\n",
            "c": "#include <stdio.h>\nint main(void){long long n;if(scanf(\"%lld\",&n)!=1)return 0;/* Check the remainder after division by two. */puts(\"false\");}\n",
        },
        "solutions": {
            "python": "n=int(input());print(str(n%2==0).lower())",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){long n=new Scanner(System.in).nextLong();System.out.println(n%2==0);}}",
            "c": "#include <stdio.h>\nint main(void){long long n;if(scanf(\"%lld\",&n)!=1)return 0;puts(n%2==0?\"true\":\"false\");}",
        },
    },
    "find-largest": {
        "category": "Arrays & Hashing", "entry": "main.py",
        "description": "Read n followed by n integers. Print the largest value. n is at least one.",
        "tests": [{"input": "3\n2 8 3\n", "expected_output": "8"}, {"input": "3\n-4 -1 -9\n", "expected_output": "-1"}, {"input": "1\n5\n", "expected_output": "5"}],
        "examples": [{"input": "3\n2 8 3", "output": "8"}], "constraints": ["1 <= n <= 100,000"],
        "starters": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));nums=d[1:1+d[0]]\n# Track the largest value seen so far.\nprint(nums[0])\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();/* Compare each number with the current maximum. */System.out.println(0);}}\n",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;/* Track the maximum among n values. */puts(\"0\");}\n",
        },
        "solutions": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));print(max(d[1:1+d[0]]))",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long best=Long.MIN_VALUE;for(int i=0;i<n;i++)best=Math.max(best,s.nextLong());System.out.println(best);}}",
            "c": "#include <stdio.h>\n#include <limits.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long v,best=LLONG_MIN;for(int i=0;i<n;i++){scanf(\"%lld\",&v);if(v>best)best=v;}printf(\"%lld\\n\",best);}",
        },
    },
    "factorial": {
        "category": "Recursion & DP", "entry": "main.py",
        "description": "Read n and print n factorial. Define 0! as 1. Use a recursive solution or explain how recursion can be replaced by iteration.",
        "tests": [{"input": "0\n", "expected_output": "1"}, {"input": "1\n", "expected_output": "1"}, {"input": "5\n", "expected_output": "120"}],
        "examples": [{"input": "5", "output": "120"}], "constraints": ["0 <= n <= 20"],
        "starters": {
            "python": "n=int(input())\ndef factorial(n):\n    # Add a base case and a smaller recursive call.\n    return 1\nprint(factorial(n))\n",
            "java": "import java.util.*;\npublic class Main {static long factorial(int n){/* Add a base case and recursive step. */return 1;}public static void main(String[]x){System.out.println(factorial(new Scanner(System.in).nextInt()));}}\n",
            "c": "#include <stdio.h>\nlong long factorial(int n){/* Add a base case and recursive step. */return 1;}int main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;printf(\"%lld\\n\",factorial(n));}\n",
        },
        "solutions": {
            "python": "def factorial(n):\n    if n<=1:return 1\n    return n*factorial(n-1)\nprint(factorial(int(input())))",
            "java": "import java.util.*;\npublic class Main {static long f(int n){return n<=1?1:n*f(n-1);}public static void main(String[]x){System.out.println(f(new Scanner(System.in).nextInt()));}}",
            "c": "#include <stdio.h>\nlong long f(int n){return n<=1?1:n*f(n-1);}int main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;printf(\"%lld\\n\",f(n));}",
        },
    },
    "reverse-string": {
        "category": "Strings", "entry": "main.py",
        "description": "Read one line and print its characters in reverse order. Preserve spaces and punctuation.",
        "tests": [{"input": "hello\n", "expected_output": "olleh"}, {"input": "a\n", "expected_output": "a"}, {"input": "\n", "expected_output": ""}],
        "examples": [{"input": "hello", "output": "olleh"}], "constraints": ["Line length is at most 100,000 ASCII characters."],
        "starters": {
            "python": "import sys\ntext=sys.stdin.readline().rstrip('\\n')\n# Build the characters from right to left.\nprint(text)\n",
            "java": "import java.io.*;\npublic class Main {public static void main(String[]x)throws Exception{String text=new BufferedReader(new InputStreamReader(System.in)).readLine();/* Reverse the line. */System.out.println(text==null?\"\":text);}}\n",
            "c": "#include <stdio.h>\n#include <string.h>\nint main(void){char s[100005];if(!fgets(s,sizeof(s),stdin))return 0;/* Print the characters from right to left. */}\n",
        },
        "solutions": {
            "python": "print(input()[::-1])",
            "java": "import java.io.*;\npublic class Main {public static void main(String[]x)throws Exception{String s=new BufferedReader(new InputStreamReader(System.in)).readLine();if(s==null)s=\"\";System.out.println(new StringBuilder(s).reverse());}}",
            "c": "#include <stdio.h>\n#include <string.h>\nint main(void){char s[100005];if(!fgets(s,sizeof(s),stdin))return 0;int n=(int)strlen(s);if(n&&s[n-1]=='\\n')n--;for(int i=n-1;i>=0;i--)putchar(s[i]);putchar('\\n');}",
        },
    },
    "fibonacci": {
        "category": "Recursion & DP", "entry": "main.py",
        "description": "Read n and print the nth Fibonacci number, using F(0)=0 and F(1)=1. Prefer an iterative solution.",
        "tests": [{"input": "0\n", "expected_output": "0"}, {"input": "1\n", "expected_output": "1"}, {"input": "6\n", "expected_output": "8"}, {"input": "10\n", "expected_output": "55"}],
        "examples": [{"input": "6", "output": "8"}], "constraints": ["0 <= n <= 92"],
        "starters": {
            "python": "n=int(input())\n# Keep the previous two Fibonacci values.\nprint(n)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){int n=new Scanner(System.in).nextInt();/* Build the sequence using two values. */System.out.println(n);}}\n",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;/* Build the sequence using two values. */printf(\"%d\\n\",n);}\n",
        },
        "solutions": {
            "python": "n=int(input());a,b=0,1\nfor _ in range(n):a,b=b,a+b\nprint(a)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){int n=new Scanner(System.in).nextInt();long a=0,b=1;for(int i=0;i<n;i++){long t=a+b;a=b;b=t;}System.out.println(a);}}",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;unsigned long long a=0,b=1;for(int i=0;i<n;i++){unsigned long long t=a+b;a=b;b=t;}printf(\"%llu\\n\",a);}",
        },
    },
    "remove-duplicates": {
        "category": "Arrays & Hashing", "entry": "main.py",
        "description": "Read n followed by n integers. Print unique values in first-seen order, separated by spaces.",
        "tests": [{"input": "5\n1 2 1 3 2\n", "expected_output": "1 2 3"}, {"input": "3\n4 4 4\n", "expected_output": "4"}, {"input": "0\n", "expected_output": ""}],
        "examples": [{"input": "5\n1 2 1 3 2", "output": "1 2 3"}], "constraints": ["0 <= n <= 100,000"],
        "starters": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];values=d[1:1+n]\n# Keep only the first occurrence of each value.\nprint(*[])\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();/* Preserve first-seen order while removing repeats. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;/* Preserve first-seen order while removing repeats. */}\n",
        },
        "solutions": {
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));seen=set();out=[]\nfor v in d[1:1+d[0]]:\n if v not in seen:seen.add(v);out.append(v)\nprint(*out)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();Set<Integer>seen=new HashSet<>();StringBuilder out=new StringBuilder();for(int i=0;i<n;i++){int v=s.nextInt();if(seen.add(v)){if(out.length()>0)out.append(' ');out.append(v);}}System.out.println(out);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)(n?n:1)*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int first=1;for(int i=0;i<n;i++){int seen=0;for(int j=0;j<i;j++)if(a[j]==a[i])seen=1;if(!seen){printf(\"%s%d\",first?\"\":\" \",a[i]);first=0;}}putchar('\\n');free(a);}",
        },
    },
    "java-sum": {
        "category": "Input & Arithmetic", "entry": "main.py",
        "description": "Read two integers and print their sum. You may write the solution in C, Python, or Java.",
        "tests": [{"input": "12 5\n", "expected_output": "17"}, {"input": "0 -4\n", "expected_output": "-4"}, {"input": "1000 999\n", "expected_output": "1999"}],
        "examples": [{"input": "12 5", "output": "17"}], "constraints": ["Both inputs fit in a signed 32-bit integer."],
        "starters": {
            "python": "a,b=map(int,input().split())\n# Print the sum.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);/* Read and add two integers. */System.out.println(0);}}\n",
            "c": "#include <stdio.h>\nint main(void){long long a,b;if(scanf(\"%lld%lld\",&a,&b)!=2)return 0;/* Print their sum. */puts(\"0\");}\n",
        },
        "solutions": {
            "python": "a,b=map(int,input().split());print(a+b)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);System.out.println((long)s.nextInt()+s.nextInt());}}",
            "c": "#include <stdio.h>\nint main(void){long long a,b;if(scanf(\"%lld%lld\",&a,&b)!=2)return 0;printf(\"%lld\\n\",a+b);}",
        },
    },
    "temperature-converter": {
        "category": "Input & Arithmetic", "entry": "main.py",
        "description": "Read a Celsius temperature and print its Fahrenheit equivalent to exactly two decimal places. Formula: F = C * 9 / 5 + 32.",
        "tests": [{"input": "0\n", "expected_output": "32.00"}, {"input": "100\n", "expected_output": "212.00"}, {"input": "-40\n", "expected_output": "-40.00"}],
        "examples": [{"input": "25", "output": "77.00"}], "constraints": ["-10,000 <= Celsius <= 10,000"],
        "starters": {
            "python": "celsius=float(input())\n# Convert Celsius to Fahrenheit and print two decimals.\nprint(0.0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){double c=new Scanner(System.in).nextDouble();/* Convert and format to two decimals. */System.out.printf(java.util.Locale.US,\"%.2f%n\",0.0);}}\n",
            "c": "#include <stdio.h>\nint main(void){double c;if(scanf(\"%lf\",&c)!=1)return 0;/* Convert and print two decimal places. */printf(\"%.2f\\n\",0.0);}\n",
        },
        "solutions": {
            "python": "c=float(input());print(f'{c*9/5+32:.2f}')",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){double c=new Scanner(System.in).nextDouble();System.out.printf(Locale.US,\"%.2f%n\",c*9.0/5+32);}}",
            "c": "#include <stdio.h>\nint main(void){double c;if(scanf(\"%lf\",&c)!=1)return 0;printf(\"%.2f\\n\",c*9.0/5+32);}",
        },
    },
    "c-square": {
        "category": "Math & Logic", "entry": "main.py",
        "description": "Read an integer and print its square. You may write the solution in C, Python, or Java.",
        "tests": [{"input": "7\n", "expected_output": "49"}, {"input": "0\n", "expected_output": "0"}, {"input": "-3\n", "expected_output": "9"}],
        "examples": [{"input": "7", "output": "49"}], "constraints": ["Input is between -1,000,000 and 1,000,000."],
        "starters": {
            "python": "n=int(input())\n# Square the number.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){long n=new Scanner(System.in).nextLong();/* Print the square. */System.out.println(0);}}\n",
            "c": "#include <stdio.h>\nint main(void){long long n;if(scanf(\"%lld\",&n)!=1)return 0;/* Print n times n. */puts(\"0\");}\n",
        },
        "solutions": {
            "python": "n=int(input());print(n*n)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){long n=new Scanner(System.in).nextLong();System.out.println(n*n);}}",
            "c": "#include <stdio.h>\nint main(void){long long n;if(scanf(\"%lld\",&n)!=1)return 0;printf(\"%lld\\n\",n*n);}",
        },
    },
}


def upgrade_exercise(exercise: dict) -> dict:
    """Convert a seeded console exercise into the shared three-language format."""
    spec = FUNDAMENTALS.get(exercise["id"])
    if not spec:
        return exercise
    exercise.update({
        "description": spec["description"],
        "tests": spec["tests"],
        "starter_code": spec["starters"]["python"],
        "solution": spec["solutions"]["python"],
        "concept": spec["category"],
        "category": spec["category"],
        "language": "multi",
        "execution_mode": "multi_language_stdio",
        "entry_point": "main.py",
        "language_starters": spec["starters"],
        "language_solutions": spec["solutions"],
        "examples": spec["examples"],
        "constraints": spec["constraints"],
    })
    return exercise


def build_additional_exercises() -> list[dict]:
    """Create extra language-neutral fundamentals not present in the old seed."""
    titles = {
        "running-sum": ("Running Sum", "Beginner", ["array", "loops", "prefix sum"]),
        "temperature-converter": ("Temperature Converter", "Beginner", ["input", "arithmetic", "formatting"]),
    }
    result = []
    for exercise_id, (title, difficulty, tags) in titles.items():
        spec = FUNDAMENTALS[exercise_id]
        result.append({
            "id": exercise_id,
            "title": title,
            "description": spec["description"],
            "starter_code": spec["starters"]["python"],
            "function_name": "",
            "tests": spec["tests"],
            "solution": spec["solutions"]["python"],
            "concept": spec["category"],
            "category": spec["category"],
            "difficulty": difficulty,
            "tags": tags,
            "language": "multi",
            "execution_mode": "multi_language_stdio",
            "entry_point": "main.py",
            "language_starters": spec["starters"],
            "language_solutions": spec["solutions"],
            "examples": spec["examples"],
            "constraints": spec["constraints"],
        })
    return result

