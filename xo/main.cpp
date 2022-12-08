#include <iostream>

using namespace std;

const unsigned short rows{3};
const unsigned short columns{3};
char board[rows][columns];




void get_input(char board[][columns],unsigned short &row,unsigned short &column);

void display_board(char board[][columns], unsigned short rows, unsigned short columns);

bool is_game_over(char board[][columns],unsigned short rows,unsigned short columns);

int main(){
    
    //initialize all cells of the board to the character N 

    for(unsigned short r{0};r<rows;++r){
        for(unsigned short c{0};c<columns;++c)
            board[r][c] = 'N';
    }

    unsigned short counter{0};
    unsigned short row{0};
    unsigned short column{0};
    
 
    display_board(board,rows,columns);
    char player;
    bool game_over{false};
    
    do{
        
        player = (counter%2 == 0)? 'X' : 'O';

        get_input(board,row,column);

        board[row][column] = player;
        
        display_board(board,rows,columns);
        
        game_over = is_game_over(board,rows,columns) ;
        
        if(game_over)
            cout << "\nPlayer " << player << " Won!!!" << endl;
        else
            ++counter;
        
    }while( (!game_over)&&(counter!= (rows)*(columns) ) );
    
    if(counter == (rows)*(columns) )
        cout << "\nDraw!!!" << endl;
    
    
    return 0;
}


inline void format_blocks(unsigned short columns, bool is_last_row=false){
    for(unsigned short c{0};c<columns+2;++c)
        if( (c==0) || (c==columns+1) )
            cout << '#';
        else{
            if (is_last_row)
                cout << '#';
            else
                cout << c-1;
        }
    cout << endl;
}

void display_board(char board[][columns], unsigned short rows,unsigned short columns){
    
    system("clear");
    
    format_blocks(columns);
    
    for(unsigned short r{0};r<rows;++r){
        for(unsigned short c{0};c<columns+2;++c){
            if(c==0)
                 cout << r;
            else if (c==columns+1)  // if we are in the edge columns display # for formating
                cout << '#';
            else
                cout << board[r][c-1];
        }
        cout << endl;
    }
    
    format_blocks(columns,true);
    
}



void get_input(char board[][columns],unsigned short &row,unsigned short &column){
        
        unsigned short temp_row{0},temp_col{0};
        
        do{
            cout << "Enter the row number: ";
            cin >> temp_row;
            
            cout << "Enter the column number: ";
            cin >> temp_col;
            
        }while( (temp_row>=rows) || (temp_col>=columns) || (board[temp_row][temp_col]!='N'));
        
        row = temp_row;
        column = temp_col;
        
}

bool check_row(char board[][columns],unsigned short columns,unsigned short row);    //check game over on a single row
bool check_column(char board[][columns],unsigned short rows,unsigned short column);
bool check_diognal(char board[][columns],unsigned short rows,unsigned short columns);

bool is_game_over(char board[][columns],unsigned short rows,unsigned short columns){
    
    
    for(unsigned short r{0};r<rows;++r){
        if(check_row(board,columns,r) )
            return true;
    }
    
    for(unsigned short c{0};c<columns;++c){
        if(check_column(board,rows,c) )
            return true;
    }
    
    return check_diognal(board,rows,columns);
}


bool check_row(char board[][columns],unsigned short columns,unsigned short row){
    
    unsigned short c{1};
    
    if(board[row][c-1]!='N'){
    
        for(;c<columns,board[row][c]==board[row][c-1];++c)
            ;
        
        
        if(c==columns)    //if we reached the end of row then we know that the row is valid
            return true;
        else
            return false;
    }else
        return false;
}

bool check_column(char board[][columns],unsigned short rows,unsigned short column){
    
    unsigned short r {1};
    
    if(board[r-1][column]!='N'){
        for(;r<rows,board[r][column]==board[r-1][column];++r)
            ;
        

        if(r==rows)   
            return true;
        else
            return false;
    }else
        return false;
}


bool check_diognal(char board[][columns],unsigned short rows,unsigned short columns){
    
    bool left_diog{false},right_diog{false};
    
    unsigned short c{1},r{1};
    if(board[r-1][c-1]!='N'){
        
        for(;c<columns,r<rows,board[r][c]==board[r-1][c-1];++r,++c)
            ;
        
        if(r==rows)
            left_diog = true;
    }else
        left_diog = false;
    
    
    
    c = 1;
    r = rows-1;
    if(board[r][c-1]!='N'){
        
        for(;c<columns,r>0,board[r][c]==board[r-1][c-1];--r,++c)
            ;
        
        if(c==columns)
            right_diog = true;
    }else
        right_diog = false;
    
    return left_diog || right_diog;
}



