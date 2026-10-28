"""Additional categorized, three-language judge problems."""

from .dsa_catalog import problem


EXTRA_DSA_EXERCISES = [
    problem(
        id="dsa-contains-duplicate", title="Contains Duplicate", category="Arrays & Hashing", difficulty="Easy",
        description="Given n integers, print true if any value occurs at least twice; otherwise print false. Input: n followed by n integers.",
        examples=[{"input": "4\n1 2 3 1", "output": "true"}],
        constraints=["1 <= n <= 100,000", "Values fit in a signed 32-bit integer."],
        tests=[{"input": "4\n1 2 3 1\n", "expected_output": "true"}, {"input": "4\n1 2 3 4\n", "expected_output": "false"}, {"input": "3\n0 0 1\n", "expected_output": "true"}],
        starters={
            "python": "import sys\ndata=list(map(int,sys.stdin.buffer.read().split())); n=data[0]; a=data[1:1+n]\nprint(str(len(set(a))<n).lower())\n",
            "java": "import java.util.*;\npublic class Main { public static void main(String[] x){Scanner s=new Scanner(System.in);int n=s.nextInt();Set<Integer> seen=new HashSet<>();boolean dup=false;for(int i=0;i<n;i++)if(!seen.add(s.nextInt()))dup=true;System.out.println(dup);}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int dup=0;for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(a[i]==a[j])dup=1;puts(dup?\"true\":\"false\");free(a);}\n",
        },
        solutions={
            "python": "import sys\ndata=list(map(int,sys.stdin.buffer.read().split()));n=data[0];a=data[1:1+n]\nprint(str(len(set(a))<n).lower())",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();Set<Integer> seen=new HashSet<>();boolean d=false;for(int i=0;i<n;i++)if(!seen.add(s.nextInt()))d=true;System.out.println(d);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int d=0;for(int i=0;i<n;i++)for(int j=0;j<i;j++)if(a[i]==a[j])d=1;puts(d?\"true\":\"false\");free(a);}",
        }, tags=["array", "hash set", "duplicates"],
    ),
    problem(
        id="dsa-product-except-self", title="Product of Array Except Self", category="Arrays & Hashing", difficulty="Medium",
        description="For each array position, print the product of every other value. Do not use division. Input: n followed by n integers.",
        examples=[{"input": "4\n1 2 3 4", "output": "24 12 8 6"}],
        constraints=["2 <= n <= 100,000", "Test products fit in a signed 64-bit integer."],
        tests=[{"input": "4\n1 2 3 4\n", "expected_output": "24 12 8 6"}, {"input": "3\n-1 1 0\n", "expected_output": "0 0 -1"}, {"input": "2\n3 5\n", "expected_output": "5 3"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n]\n# Build prefix and suffix products.\nprint()\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long[]a=new long[n];for(int i=0;i<n;i++)a[i]=s.nextLong();/* Build prefix and suffix products. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long*a=malloc((size_t)n*sizeof(long long));for(int i=0;i<n;i++)scanf(\"%lld\",&a[i]);/* Build prefix and suffix products. */free(a);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];r=[1]*n;p=1\nfor i in range(n):r[i]=p;p*=a[i]\np=1\nfor i in range(n-1,-1,-1):r[i]*=p;p*=a[i]\nprint(*r)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long[]a=new long[n],r=new long[n];for(int i=0;i<n;i++)a[i]=s.nextLong();long p=1;for(int i=0;i<n;i++){r[i]=p;p*=a[i];}p=1;for(int i=n-1;i>=0;i--){r[i]*=p;p*=a[i];}for(int i=0;i<n;i++)System.out.print((i>0?\" \":\"\")+r[i]);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long*a=malloc((size_t)n*sizeof(long long)),*r=malloc((size_t)n*sizeof(long long));for(int i=0;i<n;i++)scanf(\"%lld\",&a[i]);long long p=1;for(int i=0;i<n;i++){r[i]=p;p*=a[i];}p=1;for(int i=n-1;i>=0;i--){r[i]*=p;p*=a[i];}for(int i=0;i<n;i++)printf(\"%s%lld\",i?\" \":\"\",r[i]);free(a);free(r);}",
        }, tags=["array", "prefix product", "suffix product"],
    ),
    problem(
        id="dsa-move-zeroes", title="Move Zeroes", category="Two Pointers", difficulty="Easy",
        description="Move every zero to the end while keeping the relative order of nonzero values. Input: n followed by n integers; print the resulting array.",
        examples=[{"input": "5\n0 1 0 3 12", "output": "1 3 12 0 0"}],
        constraints=["1 <= n <= 100,000"],
        tests=[{"input": "5\n0 1 0 3 12\n", "expected_output": "1 3 12 0 0"}, {"input": "3\n0 0 1\n", "expected_output": "1 0 0"}, {"input": "4\n1 2 3 4\n", "expected_output": "1 2 3 4"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n]\n# Compact nonzero values, then append zeroes.\nprint()\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();/* Move zeroes in place. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);/* Move zeroes while preserving order. */free(a);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];r=[x for x in a if x!=0];r += [0]*(n-len(r));print(*r)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();int w=0;for(int v:a)if(v!=0)a[w++]=v;while(w<n)a[w++]=0;for(int i=0;i<n;i++)System.out.print((i>0?\" \":\"\")+a[i]);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int w=0;for(int i=0;i<n;i++)if(a[i]!=0)a[w++]=a[i];while(w<n)a[w++]=0;for(int i=0;i<n;i++)printf(\"%s%d\",i?\" \":\"\",a[i]);free(a);}",
        }, tags=["array", "in-place", "two pointers"],
    ),
    problem(
        id="dsa-container-water", title="Container With Most Water", category="Two Pointers", difficulty="Medium",
        description="Choose two vertical lines that hold the most water. Area is the distance between them times the shorter height. Input: n followed by n heights.",
        examples=[{"input": "9\n1 8 6 2 5 4 8 3 7", "output": "49"}],
        constraints=["2 <= n <= 100,000", "0 <= height[i] <= 1,000,000,000"],
        tests=[{"input": "9\n1 8 6 2 5 4 8 3 7\n", "expected_output": "49"}, {"input": "2\n1 1\n", "expected_output": "1"}, {"input": "4\n1 2 1 3\n", "expected_output": "4"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];h=d[1:1+n]\n# Move the pointer at the shorter line.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]h=new int[n];for(int i=0;i<n;i++)h[i]=s.nextInt();/* Use two pointers. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long*h=malloc((size_t)n*sizeof(long long));for(int i=0;i<n;i++)scanf(\"%lld\",&h[i]);/* Use two pointers. */free(h);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];h=d[1:1+n];l=0;r=n-1;best=0\nwhile l<r:\n best=max(best,(r-l)*min(h[l],h[r]))\n if h[l]<h[r]:l+=1\n else:r-=1\nprint(best)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]h=new int[n];for(int i=0;i<n;i++)h[i]=s.nextInt();int l=0,r=n-1;long best=0;while(l<r){best=Math.max(best,(long)(r-l)*Math.min(h[l],h[r]));if(h[l]<h[r])l++;else r--;}System.out.println(best);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long*h=malloc((size_t)n*sizeof(long long));for(int i=0;i<n;i++)scanf(\"%lld\",&h[i]);int l=0,r=n-1;long long best=0;while(l<r){long long height=h[l]<h[r]?h[l]:h[r],area=(long long)(r-l)*height;if(area>best)best=area;if(h[l]<h[r])l++;else r--;}printf(\"%lld\\n\",best);free(h);}",
        }, tags=["array", "two pointers", "greedy"],
    ),
    problem(
        id="dsa-daily-temperatures", title="Daily Temperatures", category="Stack", difficulty="Medium",
        description="For each day, print how many days must pass before a warmer temperature. If no warmer day exists, print 0. Input: n followed by n temperatures.",
        examples=[{"input": "8\n73 74 75 71 69 72 76 73", "output": "1 1 4 2 1 1 0 0"}],
        constraints=["1 <= n <= 100,000", "-100 <= temperature[i] <= 100"],
        tests=[{"input": "8\n73 74 75 71 69 72 76 73\n", "expected_output": "1 1 4 2 1 1 0 0"}, {"input": "4\n30 40 50 60\n", "expected_output": "1 1 1 0"}, {"input": "3\n50 40 30\n", "expected_output": "0 0 0"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];t=d[1:1+n]\n# Keep indices of days waiting for a warmer value.\nprint(*([0]*n))\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]t=new int[n];for(int i=0;i<n;i++)t[i]=s.nextInt();/* Use a monotonic stack of indices. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*t=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&t[i]);/* Use a monotonic stack of indices. */free(t);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];t=d[1:1+n];r=[0]*n;st=[]\nfor i,v in enumerate(t):\n while st and t[st[-1]]<v:\n  j=st.pop();r[j]=i-j\n st.append(i)\nprint(*r)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]t=new int[n],r=new int[n],st=new int[n];for(int i=0;i<n;i++)t[i]=s.nextInt();int top=0;for(int i=0;i<n;i++){while(top>0&&t[st[top-1]]<t[i]){int j=st[--top];r[j]=i-j;}st[top++]=i;}for(int i=0;i<n;i++)System.out.print((i>0?\" \":\"\")+r[i]);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*t=malloc((size_t)n*sizeof(int)),*r=calloc((size_t)n,sizeof(int)),*st=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&t[i]);int top=0;for(int i=0;i<n;i++){while(top>0&&t[st[top-1]]<t[i]){int j=st[--top];r[j]=i-j;}st[top++]=i;}for(int i=0;i<n;i++)printf(\"%s%d\",i?\" \":\"\",r[i]);free(t);free(r);free(st);}",
        }, tags=["array", "stack", "monotonic stack"],
    ),
    problem(
        id="dsa-search-insert", title="Search Insert Position", category="Binary Search", difficulty="Easy",
        description="Given a sorted array and target, print the target's index, or the position where it should be inserted to keep the array sorted. Input: n, n integers, then target.",
        examples=[{"input": "4\n1 3 5 6\n2", "output": "1"}],
        constraints=["1 <= n <= 100,000", "The values are sorted in nondecreasing order."],
        tests=[{"input": "4\n1 3 5 6\n2\n", "expected_output": "1"}, {"input": "4\n1 3 5 6\n5\n", "expected_output": "2"}, {"input": "2\n1 3\n4\n", "expected_output": "2"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];target=d[1+n]\n# Narrow the candidate range by half each iteration.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();int target=s.nextInt();/* Binary search for the lower bound. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int target;scanf(\"%d\",&target);/* Binary search for the lower bound. */free(a);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];t=d[1+n];l=0;r=n\nwhile l<r:\n m=(l+r)//2\n if a[m]<t:l=m+1\n else:r=m\nprint(l)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();int t=s.nextInt(),l=0,r=n;while(l<r){int m=l+(r-l)/2;if(a[m]<t)l=m+1;else r=m;}System.out.println(l);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int t;scanf(\"%d\",&t);int l=0,r=n;while(l<r){int m=l+(r-l)/2;if(a[m]<t)l=m+1;else r=m;}printf(\"%d\\n\",l);free(a);}",
        }, tags=["array", "binary search", "lower bound"],
    ),
    problem(
        id="dsa-search-range", title="Find First and Last Position", category="Binary Search", difficulty="Medium",
        description="In a sorted array, print the first and last indices of target. Print -1 -1 when it is absent. Input: n, n integers, then target.",
        examples=[{"input": "6\n5 7 7 8 8 10\n8", "output": "3 4"}],
        constraints=["0 <= n <= 100,000", "The values are sorted in nondecreasing order."],
        tests=[{"input": "6\n5 7 7 8 8 10\n8\n", "expected_output": "3 4"}, {"input": "6\n5 7 7 8 8 10\n6\n", "expected_output": "-1 -1"}, {"input": "1\n2\n2\n", "expected_output": "0 0"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];t=d[1+n]\n# Use lower and upper bound binary searches.\nprint(-1,-1)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();int t=s.nextInt();/* Find lower and upper bounds. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)(n?n:1)*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int t;scanf(\"%d\",&t);/* Find lower and upper bounds. */free(a);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];t=d[1+n]\ndef bound(right):\n l=0;r=n\n while l<r:\n  m=(l+r)//2\n  if a[m]<t or (right and a[m]==t):l=m+1\n  else:r=m\n return l\nl=bound(False);r=bound(True)-1;print(l,r) if l<n and a[l]==t else print(-1,-1)",
            "java": "import java.util.*;\npublic class Main {static int bound(int[]a,int t,boolean right){int l=0,r=a.length;while(l<r){int m=l+(r-l)/2;if(a[m]<t||(right&&a[m]==t))l=m+1;else r=m;}return l;}public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();int t=s.nextInt(),l=bound(a,t,false);if(l==n||a[l]!=t)System.out.println(\"-1 -1\");else System.out.println(l+\" \"+(bound(a,t,true)-1));}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint bound(int*a,int n,int t,int right){int l=0,r=n;while(l<r){int m=l+(r-l)/2;if(a[m]<t||(right&&a[m]==t))l=m+1;else r=m;}return l;}int main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;int*a=malloc((size_t)(n?n:1)*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int t;scanf(\"%d\",&t);int l=bound(a,n,t,0);if(l==n||a[l]!=t)puts(\"-1 -1\");else printf(\"%d %d\\n\",l,bound(a,n,t,1)-1);free(a);}",
        }, tags=["array", "binary search", "range"],
    ),
    problem(
        id="dsa-longest-substring", title="Longest Substring Without Repeating Characters", category="Sliding Window", difficulty="Medium",
        description="Print the length of the longest substring that contains no repeated characters. Input is one line of ASCII text.",
        examples=[{"input": "abcabcbb", "output": "3"}],
        constraints=["0 <= text length <= 100,000", "Input contains printable ASCII characters."],
        tests=[{"input": "abcabcbb\n", "expected_output": "3"}, {"input": "bbbbb\n", "expected_output": "1"}, {"input": "pwwkew\n", "expected_output": "3"}],
        starters={
            "python": "import sys\ns=sys.stdin.readline().rstrip('\\n')\n# Move a window's left edge past repeated characters.\nprint(0)\n",
            "java": "import java.io.*;\npublic class Main {public static void main(String[]x)throws Exception{String s=new BufferedReader(new InputStreamReader(System.in)).readLine();/* Track last-seen positions in a sliding window. */}}\n",
            "c": "#include <stdio.h>\n#include <string.h>\nint main(void){char s[100005];if(!fgets(s,sizeof(s),stdin))s[0]=0;/* Track last-seen positions in a sliding window. */puts(\"0\");}\n",
        },
        solutions={
            "python": "import sys\ns=sys.stdin.readline().rstrip('\\n');last={};left=best=0\nfor i,c in enumerate(s):\n if c in last:left=max(left,last[c]+1)\n last[c]=i;best=max(best,i-left+1)\nprint(best)",
            "java": "import java.io.*;\npublic class Main {public static void main(String[]x)throws Exception{String s=new BufferedReader(new InputStreamReader(System.in)).readLine();if(s==null)s=\"\";int[]last=new int[128];java.util.Arrays.fill(last,-1);int left=0,best=0;for(int i=0;i<s.length();i++){char c=s.charAt(i);left=Math.max(left,last[c]+1);last[c]=i;best=Math.max(best,i-left+1);}System.out.println(best);}}",
            "c": "#include <stdio.h>\n#include <string.h>\nint main(void){char s[100005];if(!fgets(s,sizeof(s),stdin))s[0]=0;int n=(int)strlen(s);if(n&&s[n-1]=='\\n')s[--n]=0;int last[128];for(int i=0;i<128;i++)last[i]=-1;int left=0,best=0;for(int i=0;i<n;i++){unsigned char c=(unsigned char)s[i];left=left>last[c]+1?left:last[c]+1;last[c]=i;if(i-left+1>best)best=i-left+1;}printf(\"%d\\n\",best);}",
        }, tags=["string", "sliding window", "hash map"],
    ),
    problem(
        id="dsa-min-subarray", title="Minimum Size Subarray Sum", category="Sliding Window", difficulty="Medium",
        description="Given positive integers, print the shortest contiguous subarray length whose sum is at least target, or 0 if none exists. Input: target, n, then n values.",
        examples=[{"input": "7 6\n2 3 1 2 4 3", "output": "2"}],
        constraints=["1 <= n <= 100,000", "All array values and target are positive."],
        tests=[{"input": "7 6\n2 3 1 2 4 3\n", "expected_output": "2"}, {"input": "4 3\n1 4 4\n", "expected_output": "1"}, {"input": "11 5\n1 1 1 1 1\n", "expected_output": "0"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));target,n=d[:2];a=d[2:2+n]\n# Expand and shrink a running-sum window.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int target=s.nextInt(),n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();/* Expand and shrink a window. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int target,n;if(scanf(\"%d%d\",&target,&n)!=2)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);/* Expand and shrink a window. */free(a);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));target,n=d[:2];a=d[2:2+n];left=total=0;best=n+1\nfor right,v in enumerate(a):\n total+=v\n while total>=target:\n  best=min(best,right-left+1);total-=a[left];left+=1\nprint(0 if best==n+1 else best)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int target=s.nextInt(),n=s.nextInt();int[]a=new int[n];for(int i=0;i<n;i++)a[i]=s.nextInt();int left=0,best=n+1;long sum=0;for(int right=0;right<n;right++){sum+=a[right];while(sum>=target){best=Math.min(best,right-left+1);sum-=a[left++];}}System.out.println(best==n+1?0:best);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int target,n;if(scanf(\"%d%d\",&target,&n)!=2)return 0;int*a=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&a[i]);int left=0,best=n+1;long long sum=0;for(int right=0;right<n;right++){sum+=a[right];while(sum>=target){int len=right-left+1;if(len<best)best=len;sum-=a[left++];}}printf(\"%d\\n\",best==n+1?0:best);free(a);}",
        }, tags=["array", "sliding window", "two pointers"],
    ),
    problem(
        id="dsa-house-robber", title="House Robber", category="Dynamic Programming", difficulty="Medium",
        description="Each value is the money in one house. Adjacent houses cannot both be robbed. Print the maximum amount. Input: n followed by n nonnegative values.",
        examples=[{"input": "4\n1 2 3 1", "output": "4"}],
        constraints=["1 <= n <= 100,000", "0 <= value[i] <= 1,000,000,000"],
        tests=[{"input": "4\n1 2 3 1\n", "expected_output": "4"}, {"input": "5\n2 7 9 3 1\n", "expected_output": "12"}, {"input": "1\n5\n", "expected_output": "5"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n]\n# Keep best totals with and without the previous house.\nprint(0)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long[]a=new long[n];for(int i=0;i<n;i++)a[i]=s.nextLong();/* Track take and skip states. */}}\n",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long a,b,v;/* Track take and skip states. */}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));n=d[0];a=d[1:1+n];prev2=prev1=0\nfor v in a:prev2,prev1=prev1,max(prev1,prev2+v)\nprint(prev1)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int n=s.nextInt();long skip=0,take=0;for(int i=0;i<n;i++){long v=s.nextLong(),next=Math.max(take,skip+v);skip=take;take=next;}System.out.println(take);}}",
            "c": "#include <stdio.h>\nint main(void){int n;if(scanf(\"%d\",&n)!=1)return 0;long long skip=0,take=0;for(int i=0;i<n;i++){long long v;scanf(\"%lld\",&v);long long next=take>skip+v?take:skip+v;skip=take;take=next;}printf(\"%lld\\n\",take);}",
        }, tags=["dynamic programming", "array", "state transition"],
    ),
    problem(
        id="dsa-coin-change", title="Coin Change", category="Dynamic Programming", difficulty="Medium",
        description="Given coin denominations and an amount, print the fewest coins needed to make that amount, or -1 if impossible. Input: amount, n, then n positive denominations.",
        examples=[{"input": "11 3\n1 2 5", "output": "3"}],
        constraints=["0 <= amount <= 10,000", "1 <= n <= 100", "Coin values are positive integers."],
        tests=[{"input": "11 3\n1 2 5\n", "expected_output": "3"}, {"input": "3 1\n2\n", "expected_output": "-1"}, {"input": "0 1\n1\n", "expected_output": "0"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));amount,n=d[:2];coins=d[2:2+n]\n# Build the fewest-coin answer for every subtotal.\nprint(-1)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int amount=s.nextInt(),n=s.nextInt();int[]c=new int[n];for(int i=0;i<n;i++)c[i]=s.nextInt();/* Build a minimum-coin DP table. */}}\n",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int amount,n;if(scanf(\"%d%d\",&amount,&n)!=2)return 0;int*c=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&c[i]);/* Build a minimum-coin DP table. */free(c);}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));amount,n=d[:2];coins=d[2:2+n];dp=[0]+[amount+1]*amount\nfor x in range(1,amount+1):\n for c in coins:\n  if c<=x:dp[x]=min(dp[x],dp[x-c]+1)\nprint(dp[amount] if dp[amount]<=amount else -1)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int amount=s.nextInt(),n=s.nextInt();int[]c=new int[n],dp=new int[amount+1];for(int i=0;i<n;i++)c[i]=s.nextInt();Arrays.fill(dp,amount+1);dp[0]=0;for(int a=1;a<=amount;a++)for(int coin:c)if(coin<=a)dp[a]=Math.min(dp[a],dp[a-coin]+1);System.out.println(dp[amount]>amount?-1:dp[amount]);}}",
            "c": "#include <stdio.h>\n#include <stdlib.h>\nint main(void){int amount,n;if(scanf(\"%d%d\",&amount,&n)!=2)return 0;int*c=malloc((size_t)n*sizeof(int));for(int i=0;i<n;i++)scanf(\"%d\",&c[i]);int*dp=malloc((size_t)(amount+1)*sizeof(int));for(int i=0;i<=amount;i++)dp[i]=amount+1;dp[0]=0;for(int a=1;a<=amount;a++)for(int i=0;i<n;i++)if(c[i]<=a&&dp[a-c[i]]+1<dp[a])dp[a]=dp[a-c[i]]+1;printf(\"%d\\n\",dp[amount]>amount?-1:dp[amount]);free(c);free(dp);}",
        }, tags=["dynamic programming", "unbounded knapsack", "minimum"],
    ),
    problem(
        id="dsa-flood-fill", title="Flood Fill", category="Graphs", difficulty="Easy",
        description="Starting at row sr and column sc, recolor the connected region of the same original color using four-directional movement. Input: rows columns, grid values, then sr sc newColor. Print the resulting grid by row.",
        examples=[{"input": "3 3\n1 1 1\n1 1 0\n1 0 1\n1 1 2", "output": "2 2 2\n2 2 0\n2 0 1"}],
        constraints=["1 <= rows, columns <= 100", "Grid values and coordinates are nonnegative and valid."],
        tests=[{"input": "3 3\n1 1 1\n1 1 0\n1 0 1\n1 1 2\n", "expected_output": "2 2 2\n2 2 0\n2 0 1"}, {"input": "2 2\n0 0\n0 0\n0 0 0\n", "expected_output": "0 0\n0 0"}, {"input": "1 2\n0 1\n0 0 2\n", "expected_output": "2 1"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));r,c=d[:2];g=[d[2+i*c:2+(i+1)*c] for i in range(r)];sr,sc,color=d[2+r*c:5+r*c]\n# Visit only connected cells with the starting color.\nfor row in g:print(*row)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int r=s.nextInt(),c=s.nextInt();int[][]g=new int[r][c];for(int i=0;i<r;i++)for(int j=0;j<c;j++)g[i][j]=s.nextInt();int sr=s.nextInt(),sc=s.nextInt(),color=s.nextInt();/* Traverse the connected component. */}}\n",
            "c": "#include <stdio.h>\nint main(void){int r,c;if(scanf(\"%d%d\",&r,&c)!=2)return 0;int g[100][100];for(int i=0;i<r;i++)for(int j=0;j<c;j++)scanf(\"%d\",&g[i][j]);int sr,sc,color;scanf(\"%d%d%d\",&sr,&sc,&color);/* Traverse the connected component. */}\n",
        },
        solutions={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));r,c=d[:2];g=[d[2+i*c:2+(i+1)*c] for i in range(r)];sr,sc,color=d[2+r*c:5+r*c];old=g[sr][sc]\nif old!=color:\n stack=[(sr,sc)];g[sr][sc]=color\n while stack:\n  i,j=stack.pop()\n  for ni,nj in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):\n   if 0<=ni<r and 0<=nj<c and g[ni][nj]==old:g[ni][nj]=color;stack.append((ni,nj))\nfor row in g:print(*row)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int r=s.nextInt(),c=s.nextInt();int[][]g=new int[r][c];for(int i=0;i<r;i++)for(int j=0;j<c;j++)g[i][j]=s.nextInt();int sr=s.nextInt(),sc=s.nextInt(),color=s.nextInt(),old=g[sr][sc];if(old!=color){ArrayDeque<int[]>q=new ArrayDeque<>();q.push(new int[]{sr,sc});g[sr][sc]=color;int[]dr={-1,1,0,0},dc={0,0,-1,1};while(!q.isEmpty()){int[]p=q.pop();for(int k=0;k<4;k++){int a=p[0]+dr[k],b=p[1]+dc[k];if(a>=0&&a<r&&b>=0&&b<c&&g[a][b]==old){g[a][b]=color;q.push(new int[]{a,b});}}}}for(int[]row:g){for(int j=0;j<c;j++)System.out.print((j>0?\" \":\"\")+row[j]);System.out.println();}}}",
            "c": "#include <stdio.h>\nint main(void){int r,c;if(scanf(\"%d%d\",&r,&c)!=2)return 0;int g[100][100],qi[10000],qj[10000];for(int i=0;i<r;i++)for(int j=0;j<c;j++)scanf(\"%d\",&g[i][j]);int sr,sc,color;scanf(\"%d%d%d\",&sr,&sc,&color);int old=g[sr][sc];if(old!=color){int head=0,tail=0;qi[tail]=sr;qj[tail++]=sc;g[sr][sc]=color;int di[4]={-1,1,0,0},dj[4]={0,0,-1,1};while(head<tail){int i=qi[head],j=qj[head++];for(int k=0;k<4;k++){int a=i+di[k],b=j+dj[k];if(a>=0&&a<r&&b>=0&&b<c&&g[a][b]==old){g[a][b]=color;qi[tail]=a;qj[tail++]=b;}}}}for(int i=0;i<r;i++){for(int j=0;j<c;j++)printf(\"%s%d\",j?\" \":\"\",g[i][j]);if(i+1<r)putchar('\\n');}}",
        }, tags=["graph", "matrix", "breadth-first search", "depth-first search"],
    ),
    problem(
        id="dsa-rotting-oranges", title="Rotting Oranges", category="Graphs", difficulty="Medium",
        description="Each minute, rotten oranges infect adjacent fresh oranges. Print minutes until no fresh orange remains, or -1 if that is impossible. Input: rows columns followed by the grid (0 empty, 1 fresh, 2 rotten).",
        examples=[{"input": "3 3\n2 1 1\n1 1 0\n0 1 1", "output": "4"}],
        constraints=["1 <= rows, columns <= 100", "Grid cells are 0, 1, or 2."],
        tests=[{"input": "3 3\n2 1 1\n1 1 0\n0 1 1\n", "expected_output": "4"}, {"input": "3 3\n2 1 1\n0 1 1\n1 0 1\n", "expected_output": "-1"}, {"input": "1 2\n0 2\n", "expected_output": "0"}],
        starters={
            "python": "import sys\nd=list(map(int,sys.stdin.buffer.read().split()));r,c=d[:2];g=[d[2+i*c:2+(i+1)*c] for i in range(r)]\n# Start BFS from all rotten cells at minute zero.\nprint(-1)\n",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int r=s.nextInt(),c=s.nextInt();int[][]g=new int[r][c];for(int i=0;i<r;i++)for(int j=0;j<c;j++)g[i][j]=s.nextInt();/* Run multi-source BFS by minute. */System.out.println(0);}}\n",
            "c": "#include <stdio.h>\nint main(void){int r,c;if(scanf(\"%d%d\",&r,&c)!=2)return 0;int g[100][100];for(int i=0;i<r;i++)for(int j=0;j<c;j++)scanf(\"%d\",&g[i][j]);/* Run multi-source BFS by minute. */}\n",
        },
        solutions={
            "python": "import sys,collections\nd=list(map(int,sys.stdin.buffer.read().split()));r,c=d[:2];g=[d[2+i*c:2+(i+1)*c] for i in range(r)];q=collections.deque();fresh=0\nfor i in range(r):\n for j in range(c):\n  if g[i][j]==2:q.append((i,j,0))\n  elif g[i][j]==1:fresh+=1\nminutes=0\nwhile q:\n i,j,t=q.popleft();minutes=max(minutes,t)\n for a,b in ((i-1,j),(i+1,j),(i,j-1),(i,j+1)):\n  if 0<=a<r and 0<=b<c and g[a][b]==1:g[a][b]=2;fresh-=1;q.append((a,b,t+1))\nprint(minutes if fresh==0 else -1)",
            "java": "import java.util.*;\npublic class Main {public static void main(String[]x){Scanner s=new Scanner(System.in);int r=s.nextInt(),c=s.nextInt();int[][]g=new int[r][c];ArrayDeque<int[]>q=new ArrayDeque<>();int fresh=0;for(int i=0;i<r;i++)for(int j=0;j<c;j++){g[i][j]=s.nextInt();if(g[i][j]==2)q.add(new int[]{i,j,0});else if(g[i][j]==1)fresh++;}int time=0,[]dr={-1,1,0,0};}}",
            "c": "#include <stdio.h>\nint main(void){int r,c;if(scanf(\"%d%d\",&r,&c)!=2)return 0;int g[100][100],qi[10000],qj[10000],qt[10000],head=0,tail=0,fresh=0;for(int i=0;i<r;i++)for(int j=0;j<c;j++){scanf(\"%d\",&g[i][j]);if(g[i][j]==2){qi[tail]=i;qj[tail]=j;qt[tail++]=0;}else if(g[i][j]==1)fresh++;}int minutes=0,di[4]={-1,1,0,0},dj[4]={0,0,-1,1};while(head<tail){int i=qi[head],j=qj[head],t=qt[head++];if(t>minutes)minutes=t;for(int k=0;k<4;k++){int a=i+di[k],b=j+dj[k];if(a>=0&&a<r&&b>=0&&b<c&&g[a][b]==1){g[a][b]=2;fresh--;qi[tail]=a;qj[tail]=b;qt[tail++]=t+1;}}}printf(\"%d\\n\",fresh==0?minutes:-1);}",
        }, tags=["graph", "matrix", "breadth-first search", "queue"],
    ),
]

# Finish the Java reference solution separately to keep the catalog strings readable.
EXTRA_DSA_EXERCISES[-1]["language_solutions"]["java"] = """import java.util.*;
public class Main {
 public static void main(String[] x) {
  Scanner s=new Scanner(System.in); int r=s.nextInt(),c=s.nextInt(); int[][]g=new int[r][c];
  ArrayDeque<int[]>q=new ArrayDeque<>(); int fresh=0;
  for(int i=0;i<r;i++)for(int j=0;j<c;j++){g[i][j]=s.nextInt();if(g[i][j]==2)q.add(new int[]{i,j,0});else if(g[i][j]==1)fresh++;}
  int time=0;int[]dr={-1,1,0,0},dc={0,0,-1,1};
  while(!q.isEmpty()){int[]p=q.remove();time=Math.max(time,p[2]);for(int k=0;k<4;k++){int a=p[0]+dr[k],b=p[1]+dc[k];if(a>=0&&a<r&&b>=0&&b<c&&g[a][b]==1){g[a][b]=2;fresh--;q.add(new int[]{a,b,p[2]+1});}}}
  System.out.println(fresh==0?time:-1);
 }
}"""


