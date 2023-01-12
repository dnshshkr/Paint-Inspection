#include<iostream>
using namespace std;
extern "C"{
    void awani(void);
    int main()
    {
        awani();
        system("pause");
        return 0;
    }
    void awani()
    {
        cout<<"awani cantik"<<endl;
    }
}
