// LambdaExpressionPractice.cpp : Defines the entry point for the console application.
//

#include <cstdlib>
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Practice for capturing class's data member.
class MyClassA
{
public:
    MyClassA()
        : m_Data( 1 )
    {
    }

    int doSomething()
    {
        int result = [this]( int a )
        {
            m_Data += 1; // Change m_Data to 2.
            return a + m_Data;
        }( 100 );

        cout << "m_Data: " << m_Data << endl;
        // m_Data became 2.

        return result;
    }


    int m_Data;
};

int main()
{

#ifdef DEBUG
    cout << "This is debug build!" << endl;
#elif defined RELEASE
    cout << "This is release build!" << endl;
#else
    cout << "Cannot read DEFINES from WAF!" << endl;
#endif

    int a = 1;
    int b = 2;

    auto n1 = [] ( int a, int b )
    {
        return a + b;
    };

    int n2 = []( int a, int b )
    {
        return a + b;
    }( 5, 4 );

    cout << "Output n1: "<< n1(1 ,2) << endl;

    cout << "Output n2: " << n2 << endl;

    cout << endl;

    int c = 100;
    int d = 1000;

    // Practice using mutable
    auto n3 = [=] ( int a, int b ) mutable
    {
        // c and d here are copies of the outside variables c and d.
        // mutable allows copies to be modified, but not originals
        c *= 2; // need mutable
        d *= 2; // need mutable

        a += c;
        b += d;
        return a + b;
    };

    cout << "Output n3: " << n3( 3, 4 ) << "." << endl;
    cout << "c: " << c << ", d: " << d << endl;
    // c is still 3 and d is still 4 here.

    // Re-call n3 again. The c and d still keep the previous modification within the Lambada
    cout << "2nd Output n3: " << n3( 3, 4 ) << "." << endl;
    cout << "c: " << c << ", d: " << d << endl;

    cout << endl;

    // Practice capture by reference
    auto n4 = [&]( int a, int b )
    {
        c *= 3;
        d *= 3;

        a += c;
        b += d;
        return a + b;
    };

    cout << "Output n4: " << n4( 1, 2 ) << "." << endl;
    cout << "c: " << c << ", d: " << d << endl;
    // c became 300 and d became 3000.

    cout << endl;

    // Practice mix of "capture by reference" and "capture by value"
    // d will be "capture by value" and others will be "capture by reference".
    auto n5 = [&, d]( int a, int b ) mutable
    {
        c *= 100;
        d *= 10;

        a += c;
        b += d;
        return a + b;
    };
    cout << "Output n5: " << n5( 1, 2 ) << "." << endl;
    cout << "c: " << c << ", d: " << d << endl;
    // c became 30000 and d remains 3000.

    cout << endl;
    cout << "Reset c and d..." << endl;
    c = 100;
    d = 1000;
    cout << endl;

    // c use "pass by reference".
    auto n6 = [=, &c]( int a, int b ) mutable
    {
        c *= 10;
        d *= 10;

        a += c;
        b += d;
        return a + b;
    };
    cout << "Output n6: " << n6( 1, 2 ) << "." << endl;
    cout << "c: " << c << ", d: " << d << endl;
    // c became 1000 and d remains 1000.


    vector<int> numbers{ 1, 2, 3, 4, 5, 10, 15, 20, 25, 35, 45, 50 };
    auto count = count_if( numbers.begin(), numbers.end(),
        []( int x ) { return ( x > 5 ); } );

    cout << "Count: " << count << endl; // should 7
    cout << endl;

    MyClassA obj;
    cout << "DoSomthing: " << obj.doSomething() << endl;

    system( "pause" );
    return 0;
}

