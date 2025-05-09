package com.asiainfo.utils;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import java.util.List;

@Data
public class MailParam {

    /**
     * 收件人列表
     */
    @NotEmpty(message = "邮件收件人不能为空")
    private List<String> tos;

    /**
     * 抄送人列表（carbon copy）
     */
    private List<String> ccs;

    /**
     * 标题
     */
    private String title;

    /**
     * 内容
     */
    @NotBlank(message = "邮件内容不能为空")
    private String content;

    /**
     * 附件名称
     */
    private String attachmentName;

    /**
     * 附件内容
     */
    private byte[] attachment;

}
