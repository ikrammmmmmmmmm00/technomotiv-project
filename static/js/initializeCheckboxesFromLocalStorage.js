document.addEventListener('DOMContentLoaded', function () {
    

    function initializeCheckboxesFromLocalStorage(){
        const serializedList = localStorage.getItem('CompareIds');
        
        if (serializedList) {
            const numbersList = JSON.parse(serializedList);
            console.log(numbersList, 'saving to localstoragee'); 
    
            const checkboxes = document.querySelectorAll('.checkie');
            checkboxes.forEach(checkbox => {
                const value = checkbox.value;
                if ((numbersList).includes(value)) {
                    checkbox.checked = true;
                    console.log(checkbox.checked)
                }
            });
        } else {
            console.log('No list of numbers found in localStorage');
        }
    }
    function initializeInquiryCheckboxesFromLocalStorage(){
        const serializedList = localStorage.getItem('InquiryIds');
        
        if (serializedList) {
            const numbersList = JSON.parse(serializedList);
            console.log(numbersList, 'saving to localstorage Inquiry');
            const checkboxes = document.querySelectorAll('.inkie');

            checkboxes.forEach(checkbox => {
                const value = checkbox.value;
                if ((numbersList).includes(value)) {
                    checkbox.checked = true;
                    console.log(checkbox.checked)
                }
            });
            
        } else {
            console.log('No list of numbers found in localStorage');
        }
    }
    function updateCheckedList(ids) {
        $('.hidden_ids').val(ids.join(","))
        $('.compare_len_btn').html(ids.length)
    }
    function UpdatingCompareIds(){
        const serializedLists = localStorage.getItem('CompareIds')
        var list_ids = serializedLists ? JSON.parse(serializedLists) : []

        updateCheckedList(list_ids)
    }
    
    initializeCheckboxesFromLocalStorage()
    initializeInquiryCheckboxesFromLocalStorage()
    UpdatingCompareIds()
    $('.checkie').change(function () {
        const serializedList = localStorage.getItem('CompareIds')
        var list_ids = serializedList ? JSON.parse(serializedList) : []

        check = $(this).is(':checked')
        const id = $(this).attr('id')

        if (check) {
            list_ids.push(id);
        } else {
            const a = []
            for (var b = 0; b < list_ids.length; b++) {
                if (list_ids[b] !== id) a.push(list_ids[b])
            }
            list_ids = a
        }
        console.log(list_ids,'compareids in inquiry')
        updateCheckedList(list_ids)
        localStorage.setItem('CompareIds', JSON.stringify(list_ids))
    
    });
});

