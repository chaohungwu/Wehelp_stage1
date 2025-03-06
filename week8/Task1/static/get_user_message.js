async function get_user_message(){
    let response = await fetch("/member/message_get");
    let data =await response.json();
    // console.log(data);

    //先把留言板清空(避免沒留言資料直接點按鈕，留言然後出現兩行)
    let a = document.querySelectorAll('.message_arr');
    for(let n =0 ; n<a.length; n++){
        a[n].remove()
    };

    for(let i=0; i<data['message'].length; i++){
        let message_id = data['message'][i][2]

        let message_arr_dom = document.createElement("div");
        message_arr_dom.className = "message_arr";
        message_arr_dom.id = `message_arr_${message_id}`;
        document.querySelector("#all_message_board_content").appendChild(message_arr_dom)

        let message_name_dom = document.createElement("a");
        let message_board_name = data['message'][i][0]
        message_name_dom.textContent = `${message_board_name}:`,//插入名稱
        message_name_dom.className = "message_name";
        document.querySelector(`#message_arr_${message_id}`).appendChild(message_name_dom)

        let message_dom = document.createElement("a");
        let message_board_message = data['message'][i][1]
        message_dom.textContent = message_board_message,//插入留言
        message_dom.className = "message";
        document.querySelector(`#message_arr_${message_id}`).appendChild(message_dom)
        
        //這邊辨識這個留言是不是這個人留的
        if(data['message'][i][3] == data['siginin_id']){
            let del_but = document.createElement("button");
            del_but.textContent="X"
            del_but.className = "del_message_but";
            del_but.id = `del_message_but_${message_id}`;

            del_but.addEventListener('click', function() {
                                    let name_id = sessionStorage.getItem("name_id");//從session取出姓名資訊
                                    message_index = this.id.split("_")[3];

                                    let del_confirm = confirm('確定要刪除留言嗎?');
                                            if (del_confirm){
                                                click_del_message_but(message_index)
                                            };
                                    });

            document.querySelector(`#message_arr_${message_id}`).appendChild(del_but)//新增刪除按鈕
            }

        };
    let name_welcome_dom = document.querySelector("#name_welcome");
    // console.log(data["siginin_name"])
    name_welcome_dom.textContent = `${data["siginin_name"]}，歡迎登入系統` 
}